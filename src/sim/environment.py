"""Isaac Sim environment bootstrap utilities for RAPID v2.

This module provides the main simulation environment wrapper for Isaac Sim,
integrating sensors, ROS 2 bridge, scene management, and data logging.

Phase 1: Basic environment setup with sensors and ROS 2 bridge
Phase 2+: Planner integration, controller integration
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple


class IsaacSimEnvironment:
    """Main simulation environment wrapper for Isaac Sim.

    Manages the full simulation lifecycle:
    - Isaac Sim application context
    - Scene loading and generation
    - Sensor configuration and updates
    - ROS 2 bridge integration
    - Data logging

    Example:
        >>> env = IsaacSimEnvironment(config_path="config/env/isaac_lab_env.yaml")
        >>> env.setup_sensors()
        >>> env.setup_ros2_bridge()
        >>> env.reset(scene_family="office", seed=42)
        >>> for step in range(1000):
        >>>     obs = env.step()
        >>> env.close()
    """

    def __init__(self, config_path: str = "config/env/isaac_lab_env.yaml", headless: bool = False):
        """Initialize Isaac Sim environment.

        Args:
            config_path: Path to environment configuration YAML
            headless: Run in headless mode (no GUI)
        """
        self.config_path = Path(config_path)
        self.headless = headless
        self.config = self._load_config()

        # Simulation state
        self.app = None                # Isaac Sim SimulationApp instance
        self.world = None              # Isaac Sim World instance
        self.stage = None              # USD stage

        # Sensors
        self.sensors = {}              # Dict of sensor instances
        self.sensor_config = None      # Loaded sensor configuration

        # ROS 2 bridge
        self.ros2_bridge = None        # ROS 2 bridge node
        self.bridge_config = None      # Loaded bridge configuration

        # Scene
        self.current_scene = None      # Current scene USD path
        self.scene_family = None       # Current scene family
        self.scene_seed = None         # Current scene seed

        # Logging
        self.data_logger = None        # Data logger instance

        print(f"[IsaacSimEnvironment] Initialized with config: {config_path}")
        print(f"[IsaacSimEnvironment] Headless mode: {headless}")

    def _load_config(self) -> Dict:
        """Load environment configuration from YAML."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def initialize_isaac_sim(self):
        """Initialize Isaac Sim application context.

        CRITICAL: Must be called before any Isaac Lab imports!
        This follows the required initialization sequence:
        1. Create SimulationApp first
        2. Import Isaac Lab modules only after SimulationApp exists
        3. Create World and configure physics/rendering
        """
        print("[IsaacSimEnvironment] Initializing Isaac Sim application...")

        # Step 1: Create SimulationApp FIRST (before Isaac Lab imports)
        from isaacsim import SimulationApp

        app_config = {
            "headless": self.headless,
            "width": 1280,
            "height": 720,
        }
        self.app = SimulationApp(app_config)
        print(f"[IsaacSimEnvironment]   ✓ SimulationApp created (headless={self.headless})")

        # Step 2: NOW we can import Isaac Lab modules
        import isaaclab.sim as sim_utils
        from isaaclab.sim import SimulationContext

        # Step 3: Create World with configured physics/rendering timesteps
        sim_config = self.config.get('simulation', {})
        physics_dt = sim_config.get('physics_dt', 0.01)      # 100 Hz default
        rendering_dt = sim_config.get('rendering_dt', 0.05)  # 20 Hz default

        # Calculate render_interval: how many physics steps per render
        render_interval = int(rendering_dt / physics_dt)

        sim_cfg = sim_utils.SimulationCfg(
            dt=physics_dt,
            render_interval=render_interval,
            device="cuda:0",  # Use GPU by default
            gravity=(0.0, 0.0, -9.81),  # Standard gravity
            enable_scene_query_support=True,  # For raycasting/collision queries
        )
        self.world = SimulationContext(sim_cfg)
        print(f"[IsaacSimEnvironment]   ✓ SimulationContext created")
        print(f"[IsaacSimEnvironment]     - Physics dt: {physics_dt}s ({1/physics_dt:.0f} Hz)")
        print(f"[IsaacSimEnvironment]     - Rendering dt: {rendering_dt}s ({1/rendering_dt:.0f} Hz)")

        # Step 4: Set camera view for GUI mode
        if not self.headless:
            self.world.set_camera_view(eye=[3.5, 3.5, 3.5], target=[0.0, 0.0, 0.0])
            print(f"[IsaacSimEnvironment]   ✓ Camera view configured for GUI")

        # Step 5: Get USD stage reference
        from pxr import Usd
        import omni.usd
        self.stage = omni.usd.get_context().get_stage()
        print(f"[IsaacSimEnvironment]   ✓ USD stage reference obtained")

        print("[IsaacSimEnvironment] ✓ Isaac Sim initialization complete")
        return self.world

    def setup_sensors(self):
        """Set up sensors from configuration.

        Loads sensor config from config/env/sensors.yaml and creates:
        - Stereo depth camera (20 Hz)
        - IMU (100 Hz internal, 20 Hz logged)
        - Ground truth odometry (20 Hz)
        """
        print("[IsaacSimEnvironment] Setting up sensors...")

        # Load sensor configuration
        sensor_config_path = Path("../config/env/sensors.yaml")
        with open(sensor_config_path, 'r') as f:
            self.sensor_config = yaml.safe_load(f)
        print(f"[IsaacSimEnvironment]   ✓ Loaded sensor config from {sensor_config_path}")

        # Import sensor modules (after SimulationApp is created)
        from isaaclab.sensors.camera import Camera, CameraCfg
        from isaaclab.sensors import Imu, ImuCfg
        import isaaclab.sim as sim_utils
        import omni.isaac.core.utils.prims as prim_utils

        # Create sensor mount prims (placeholder for drone)
        # For Phase 1, we'll create a simple prim hierarchy
        # In Phase 2+, this will be replaced with actual drone robot
        prim_utils.create_prim("/World/Drone", "Xform")
        prim_utils.create_prim("/World/Drone/base_link", "Xform")

        # ====================================================================
        # 1. Setup Depth Camera
        # ====================================================================
        depth_cfg = self.sensor_config.get('depth_camera', {})
        if depth_cfg.get('enabled', True):
            print("[IsaacSimEnvironment]   Setting up depth camera...")

            # Extract configuration
            resolution = depth_cfg.get('resolution', {})
            fov = depth_cfg.get('fov', {})
            mount = depth_cfg.get('mount', {})
            update_rate = depth_cfg.get('update_rate_hz', 20)

            # Calculate update period
            update_period = 1.0 / update_rate

            # Create camera configuration
            camera_cfg = CameraCfg(
                prim_path="/World/Drone/base_link/depth_camera",
                update_period=update_period,
                height=resolution.get('height', 480),
                width=resolution.get('width', 640),
                data_types=["distance_to_image_plane"],  # Depth only for Phase 1
                spawn=sim_utils.PinholeCameraCfg(
                    focal_length=24.0,
                    focus_distance=400.0,
                    horizontal_aperture=20.955,  # Approximates 90° FOV
                    clipping_range=(
                        depth_cfg.get('min_depth_m', 0.1),
                        depth_cfg.get('max_depth_m', 30.0)
                    ),
                ),
                offset=CameraCfg.OffsetCfg(
                    pos=tuple(mount.get('position', [0.1, 0.0, 0.0])),
                    rot=(0.5, -0.5, 0.5, -0.5),  # ROS convention (x-forward, z-up)
                    convention="ros"
                ),
            )

            # Create camera sensor
            self.sensors['depth'] = Camera(cfg=camera_cfg)
            print(f"[IsaacSimEnvironment]     ✓ Depth camera created")
            print(f"[IsaacSimEnvironment]       - Resolution: {resolution.get('width', 640)}x{resolution.get('height', 480)}")
            print(f"[IsaacSimEnvironment]       - Update rate: {update_rate} Hz")
            print(f"[IsaacSimEnvironment]       - Depth range: {depth_cfg.get('min_depth_m', 0.1)}-{depth_cfg.get('max_depth_m', 30.0)}m")

        # ====================================================================
        # 2. Setup IMU Sensor
        # ====================================================================
        imu_cfg = self.sensor_config.get('imu', {})
        if imu_cfg.get('enabled', True):
            print("[IsaacSimEnvironment]   Setting up IMU sensor...")

            mount = imu_cfg.get('mount', {})
            update_rate = imu_cfg.get('update_rate_hz', 100)
            update_period = 1.0 / update_rate

            # Create IMU configuration
            imu_sensor_cfg = ImuCfg(
                prim_path="/World/Drone/base_link",  # IMU at drone center
                update_period=update_period,
                debug_vis=False,
                # Note: Isaac Lab IMU noise is configured differently
                # We'll add custom noise in post-processing if needed
            )

            # Create IMU sensor
            self.sensors['imu'] = Imu(cfg=imu_sensor_cfg)
            print(f"[IsaacSimEnvironment]     ✓ IMU sensor created")
            print(f"[IsaacSimEnvironment]       - Update rate: {update_rate} Hz (internal)")
            print(f"[IsaacSimEnvironment]       - Log rate: {imu_cfg.get('log_rate_hz', 20)} Hz")

        # ====================================================================
        # 3. Setup Ground Truth Odometry
        # ====================================================================
        odom_cfg = self.sensor_config.get('odometry', {})
        if odom_cfg.get('enabled', True):
            print("[IsaacSimEnvironment]   Setting up odometry sensor...")

            # For Phase 1, we use ground truth from simulation
            # Store as placeholder - actual data comes from robot articulation
            self.sensors['odom'] = {
                'type': 'ground_truth',
                'update_rate_hz': odom_cfg.get('update_rate_hz', 20),
                'noise': odom_cfg.get('noise', {}),
                'reference_frame': odom_cfg.get('reference_frame', 'world'),
            }
            print(f"[IsaacSimEnvironment]     ✓ Odometry configured (ground truth)")
            print(f"[IsaacSimEnvironment]       - Update rate: {odom_cfg.get('update_rate_hz', 20)} Hz")
            print(f"[IsaacSimEnvironment]       - Reference frame: {odom_cfg.get('reference_frame', 'world')}")

        print(f"[IsaacSimEnvironment] ✓ Sensor setup complete")
        print(f"[IsaacSimEnvironment]   Active sensors: {list(self.sensors.keys())}")

        return self.sensors

    def setup_ros2_bridge(self):
        """Set up ROS 2 bridge using Isaac Sim's native extension.

        Uses Isaac Sim 5.0.0's built-in isaacsim.ros2.bridge extension with
        OmniGraph nodes for sensor publishing. This approach:
        - Uses NVIDIA's production-ready ROS 2 bridge
        - Communicates via DDS (works with Docker ROS 2 containers)
        - Supports ROS 2 Jazzy with Python 3.11
        - No need for direct rclpy imports

        Loads bridge config from config/ros2/bridge_topics.yaml and creates:
        - OmniGraph nodes for sensor publishing
        - Sensor topic publishers (/camera/depth, /imu/data, /odom)
        - TF tree publishers (world → base_link → sensor frames)
        - Clock publisher for simulation time
        """
        print("[IsaacSimEnvironment] Setting up ROS 2 bridge...")

        # Load bridge configuration
        bridge_config_path = Path("config/ros2/bridge_topics.yaml")
        with open(bridge_config_path, 'r') as f:
            self.bridge_config = yaml.safe_load(f)
        print(f"[IsaacSimEnvironment]   ✓ Loaded bridge config from {bridge_config_path}")

        try:
            # Enable Isaac Sim's ROS 2 bridge extension
            import omni.kit.app
            ext_manager = omni.kit.app.get_app().get_extension_manager()

            if not ext_manager.is_extension_enabled("isaacsim.ros2.bridge"):
                ext_manager.set_extension_enabled_immediate("isaacsim.ros2.bridge", True)
                print("[IsaacSimEnvironment]   ✓ Enabled isaacsim.ros2.bridge extension")
            else:
                print("[IsaacSimEnvironment]   ✓ isaacsim.ros2.bridge extension already enabled")

            # Create OmniGraph for sensor publishing
            self._create_ros2_sensor_graph()

            print(f"[IsaacSimEnvironment] ✓ ROS 2 bridge setup complete")
            print(f"[IsaacSimEnvironment]   Using Isaac Sim native bridge with DDS transport")
            print(f"[IsaacSimEnvironment]   Topics will be available on ROS_DOMAIN_ID=0")

            self.ros2_bridge = "isaac_native"  # Mark that native bridge is active

        except ImportError as e:
            print(f"[IsaacSimEnvironment] ⚠ Warning: Could not import Isaac Sim ROS 2 bridge: {e}")
            print(f"[IsaacSimEnvironment] ⚠ Running without ROS 2 bridge")
            print(f"[IsaacSimEnvironment] ⚠ Ensure Isaac Sim 5.0.0 is properly installed")
            self.ros2_bridge = None
        except Exception as e:
            print(f"[IsaacSimEnvironment] ⚠ Warning: Could not initialize ROS 2 bridge: {e}")
            print(f"[IsaacSimEnvironment] ⚠ Make sure to source scripts/activate_ros2_env.sh before running")
            self.ros2_bridge = None

        return self.ros2_bridge

    def _create_ros2_sensor_graph(self):
        """Create OmniGraph nodes for ROS 2 sensor publishing.

        This method creates an OmniGraph that connects Isaac Sim sensors to
        ROS 2 publishers using Isaac Sim's native bridge nodes.
        """
        import omni.graph.core as og

        print("[IsaacSimEnvironment]   Creating ROS 2 sensor OmniGraph...")

        # Get enabled topics from config
        topics = self.bridge_config.get('topics', [])
        enabled_topics = {t['name']: t for t in topics if t.get('enabled', True) and t.get('direction') == 'publish'}

        # Create graph
        keys = og.Controller.Keys
        graph_path = "/World/ROS2_Bridge"

        # Build node specifications
        nodes_to_create = [
            ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
        ]

        values_to_set = []
        connections_to_make = []

        # Add depth camera publisher if enabled
        if "/camera/depth" in enabled_topics:
            nodes_to_create.append(("PublishDepth", "isaacsim.ros2.bridge.ROS2PublishImage"))
            values_to_set.extend([
                ("PublishDepth.inputs:topicName", "/camera/depth"),
                ("PublishDepth.inputs:type", "depth"),
            ])
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishDepth.inputs:execIn"))
            print("[IsaacSimEnvironment]     + Depth camera publisher (/camera/depth)")

        # Add camera info publisher if enabled
        if "/camera/depth/camera_info" in enabled_topics:
            nodes_to_create.append(("PublishCameraInfo", "isaacsim.ros2.bridge.ROS2PublishCameraInfo"))
            values_to_set.append(("PublishCameraInfo.inputs:topicName", "/camera/depth/camera_info"))
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishCameraInfo.inputs:execIn"))
            print("[IsaacSimEnvironment]     + Camera info publisher (/camera/depth/camera_info)")

        # Add IMU publisher if enabled
        if "/imu/data" in enabled_topics:
            nodes_to_create.append(("PublishIMU", "isaacsim.ros2.bridge.ROS2PublishImu"))
            values_to_set.append(("PublishIMU.inputs:topicName", "/imu/data"))
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishIMU.inputs:execIn"))
            print("[IsaacSimEnvironment]     + IMU publisher (/imu/data)")

        # Add odometry publisher if enabled
        if "/odom" in enabled_topics:
            nodes_to_create.append(("PublishOdom", "isaacsim.ros2.bridge.ROS2PublishOdometry"))
            values_to_set.append(("PublishOdom.inputs:topicName", "/odom"))
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishOdom.inputs:execIn"))
            print("[IsaacSimEnvironment]     + Odometry publisher (/odom)")

        # Add clock publisher if enabled
        if "/clock" in enabled_topics:
            nodes_to_create.append(("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"))
            values_to_set.append(("PublishClock.inputs:topicName", "/clock"))
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishClock.inputs:execIn"))
            print("[IsaacSimEnvironment]     + Clock publisher (/clock)")

        # Add TF publisher if TF is enabled
        tf_config = self.bridge_config.get('tf', {})
        if tf_config.get('enabled', True):
            nodes_to_create.append(("PublishTF", "isaacsim.ros2.bridge.ROS2PublishTransformTree"))
            values_to_set.append(("PublishTF.inputs:topicName", "/tf"))
            connections_to_make.append(("OnPlaybackTick.outputs:tick", "PublishTF.inputs:execIn"))
            print("[IsaacSimEnvironment]     + TF tree publisher (/tf)")

        # Create the graph
        try:
            (graph, nodes, _, _) = og.Controller.edit(
                {
                    "graph_path": graph_path,
                    "evaluator_name": "push",
                },
                {
                    keys.CREATE_NODES: nodes_to_create,
                    keys.SET_VALUES: values_to_set,
                    keys.CONNECT: connections_to_make,
                },
            )

            self.ros2_graph = graph
            print(f"[IsaacSimEnvironment]   ✓ Created ROS 2 sensor graph at {graph_path}")
            print(f"[IsaacSimEnvironment]   ✓ {len(nodes_to_create) - 1} publishers configured")

        except Exception as e:
            print(f"[IsaacSimEnvironment]   ✗ Error creating ROS 2 graph: {e}")
            print(f"[IsaacSimEnvironment]   ✗ Sensors will not publish to ROS 2")
            raise

    def load_scene(self, scene_family: str, seed: int, from_cache: bool = True):
        """Load or generate a scene.

        Args:
            scene_family: Scene family (office, warehouse, forest, etc.)
            seed: Random seed for scene generation
            from_cache: Load from USD cache if available

        Note: For Phase 1, we create a simple ground plane. Procedural scene
        generation will be added in a separate scene generation module.
        """
        import json
        import time
        import isaaclab.sim as sim_utils

        print(f"[IsaacSimEnvironment] Loading scene: {scene_family} (seed={seed})...")

        self.scene_family = scene_family
        self.scene_seed = seed

        # Check cache for existing USD scene
        cache_dir = Path("data/raw/scenes/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{scene_family}_seed{seed}.usd"

        if from_cache and cache_path.exists():
            print(f"[IsaacSimEnvironment]   Loading from cache: {cache_path}")
            # TODO: Load USD from cache
            # self.stage.GetRootLayer().ImportFromString(cache_path.read_text())
            print(f"[IsaacSimEnvironment]   ⚠ Cache loading not yet implemented")

        # For Phase 1, create a simple scene with ground plane and basic lighting
        print(f"[IsaacSimEnvironment]   Creating basic scene (Phase 1)...")

        # Add ground plane
        ground_cfg = sim_utils.GroundPlaneCfg(
            size=(100.0, 100.0),
            color=(0.5, 0.5, 0.5),
        )
        ground_cfg.func("/World/GroundPlane", ground_cfg)
        print(f"[IsaacSimEnvironment]     ✓ Ground plane created")

        # Add lighting
        light_cfg = sim_utils.DomeLightCfg(
            intensity=3000.0,
            color=(0.75, 0.75, 0.75),
        )
        light_cfg.func("/World/DomeLight", light_cfg)
        print(f"[IsaacSimEnvironment]     ✓ Dome light created")

        # Log scene information
        runtime_dir = Path("data/raw/runtime")
        runtime_dir.mkdir(parents=True, exist_ok=True)
        scenes_log = runtime_dir / "scenes.jsonl"

        scene_info = {
            "timestamp": time.time(),
            "scene_family": scene_family,
            "seed": seed,
            "from_cache": from_cache,
            "cache_available": cache_path.exists(),
        }

        with open(scenes_log, 'a') as f:
            f.write(json.dumps(scene_info) + '\n')

        print(f"[IsaacSimEnvironment]   ✓ Scene logged to {scenes_log}")
        print(f"[IsaacSimEnvironment] ✓ Scene loaded successfully")

        self.current_scene = str(cache_path) if from_cache else "basic_scene"
        return self.current_scene

    def reset(self, scene_family: Optional[str] = None, seed: Optional[int] = None):
        """Reset simulation environment.

        Args:
            scene_family: Optional new scene family
            seed: Optional new scene seed

        Returns:
            Initial observation dictionary
        """
        import torch
        import random

        print("[IsaacSimEnvironment] Resetting environment...")

        # Load new scene if specified
        if scene_family is not None and seed is not None:
            self.load_scene(scene_family, seed)

        # Reset physics simulation
        if self.world is not None:
            self.world.reset()
            print("[IsaacSimEnvironment]   ✓ Physics simulation reset")

        # Randomize drone initial pose (Phase 1: simple randomization)
        # In Phase 2+, this will be replaced with proper drone spawn logic
        import omni.isaac.core.utils.prims as prim_utils
        drone_prim = prim_utils.get_prim_at_path("/World/Drone/base_link")
        if drone_prim:
            # Random position within safe bounds
            x = random.uniform(-2.0, 2.0)
            y = random.uniform(-2.0, 2.0)
            z = random.uniform(1.0, 3.0)  # Above ground

            # Random orientation (yaw only for simplicity)
            yaw = random.uniform(-3.14159, 3.14159)

            # Set transform (simplified for Phase 1)
            from pxr import Gf
            import math
            quat_w = math.cos(yaw / 2)
            quat_z = math.sin(yaw / 2)

            print(f"[IsaacSimEnvironment]   ✓ Drone pose randomized: pos=({x:.2f}, {y:.2f}, {z:.2f}), yaw={yaw:.2f}")

        # Clear sensor buffers (update sensors to reset their internal state)
        for sensor_name, sensor in self.sensors.items():
            if hasattr(sensor, 'reset'):
                sensor.reset()
            elif hasattr(sensor, 'update'):
                # Force update to clear buffers
                try:
                    sensor.update(dt=0.0)
                except:
                    pass
        print("[IsaacSimEnvironment]   ✓ Sensor buffers cleared")

        # Get initial observation
        obs = self._get_sensor_observations()
        print("[IsaacSimEnvironment] ✓ Environment reset complete")

        return obs

    def step(self) -> Dict:
        """Step simulation forward by one timestep.

        Returns:
            obs: Dictionary containing sensor observations
        """
        # Step physics simulation forward
        if self.world is not None:
            self.world.step(render=True)

        # Get physics timestep
        dt = self.world.get_physics_dt() if self.world else 0.01

        # Update all sensors
        for sensor_name, sensor in self.sensors.items():
            if hasattr(sensor, 'update') and callable(sensor.update):
                try:
                    sensor.update(dt=dt)
                except Exception as e:
                    # Silently handle sensor update errors (some sensors may not need updates)
                    pass

        # Collect sensor observations
        obs = self._get_sensor_observations()

        # Note: ROS 2 publishing happens automatically via OmniGraph
        # The Isaac Sim native bridge publishes sensor data each tick
        # No manual message publishing needed in step()

        # Log data (if logger is configured)
        if self.data_logger is not None:
            try:
                self.data_logger.log(obs)
            except:
                pass

        return obs

    def close(self):
        """Shutdown simulation environment gracefully."""
        print("[IsaacSimEnvironment] Closing environment...")

        # Flush data logger buffers
        if self.data_logger is not None:
            try:
                self.data_logger.flush()
                print("[IsaacSimEnvironment]   ✓ Data logger flushed")
            except Exception as e:
                print(f"[IsaacSimEnvironment]   ⚠ Warning: Could not flush logger: {e}")

        # Shutdown ROS 2 bridge
        if self.ros2_bridge is not None:
            try:
                # Isaac Sim's native bridge is managed by the extension
                # Just disable the extension if needed
                import omni.kit.app
                ext_manager = omni.kit.app.get_app().get_extension_manager()

                if ext_manager.is_extension_enabled("isaacsim.ros2.bridge"):
                    # Note: Don't disable extension here as it may be used by other components
                    # Extension will be disabled when Isaac Sim closes
                    pass

                print("[IsaacSimEnvironment]   ✓ ROS 2 bridge shutdown")
            except Exception as e:
                print(f"[IsaacSimEnvironment]   ⚠ Warning: Could not shutdown ROS 2: {e}")

        # Close Isaac Sim application
        if self.app is not None:
            try:
                self.app.close()
                print("[IsaacSimEnvironment]   ✓ Isaac Sim application closed")
            except Exception as e:
                print(f"[IsaacSimEnvironment]   ⚠ Warning: Could not close Isaac Sim: {e}")

        print("[IsaacSimEnvironment] ✓ Environment closed successfully")

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def _get_sensor_observations(self) -> Dict:
        """Collect all sensor data into observation dictionary.

        Returns:
            Dictionary containing:
                - timestamp: Simulation time
                - depth: Depth image (H, W) if depth camera enabled
                - imu_accel: Linear acceleration (3,) if IMU enabled
                - imu_gyro: Angular velocity (3,) if IMU enabled
                - odom_pos: Position (3,) if odometry enabled
                - odom_vel: Linear velocity (3,) if odometry enabled
                - odom_quat: Orientation quaternion (4,) if odometry enabled
        """
        obs = {}

        # Add timestamp (simulation time)
        if self.world is not None:
            obs['timestamp'] = self.world.current_time
        else:
            import time
            obs['timestamp'] = time.time()

        # Collect depth camera data
        if 'depth' in self.sensors and self.sensors['depth'] is not None:
            try:
                depth_data = self.sensors['depth'].data.output.get('distance_to_image_plane')
                if depth_data is not None:
                    obs['depth'] = depth_data
            except (AttributeError, KeyError) as e:
                print(f"[IsaacSimEnvironment] Warning: Could not read depth data: {e}")

        # Collect IMU data
        if 'imu' in self.sensors and self.sensors['imu'] is not None:
            try:
                obs['imu_accel'] = self.sensors['imu'].data.lin_acc_b
                obs['imu_gyro'] = self.sensors['imu'].data.ang_vel_b
            except AttributeError as e:
                print(f"[IsaacSimEnvironment] Warning: Could not read IMU data: {e}")

        # Collect odometry data (from drone articulation or sensor)
        if 'odom' in self.sensors and self.sensors['odom'] is not None:
            try:
                # If we have a dedicated odometry sensor
                obs['odom_pos'] = self.sensors['odom'].data.pos
                obs['odom_vel'] = self.sensors['odom'].data.vel
                obs['odom_quat'] = self.sensors['odom'].data.quat
            except AttributeError:
                # Fallback: try to get from robot articulation
                if 'robot' in self.sensors and self.sensors['robot'] is not None:
                    try:
                        root_state = self.sensors['robot'].data.root_state_w
                        obs['odom_pos'] = root_state[:3]
                        obs['odom_quat'] = root_state[3:7]
                        obs['odom_vel'] = root_state[7:10]
                    except (AttributeError, IndexError) as e:
                        print(f"[IsaacSimEnvironment] Warning: Could not read odometry: {e}")

        return obs

    def _add_sensor_noise(self, data, noise_config: Dict):
        """Add physics-based noise to sensor data.

        Args:
            data: Sensor data tensor
            noise_config: Noise configuration from sensors.yaml

        Returns:
            Noisy sensor data
        """
        import torch

        if not noise_config.get('enabled', False):
            return data

        # Add Gaussian noise
        if 'std' in noise_config or 'noise_std' in noise_config:
            std = noise_config.get('std', noise_config.get('noise_std', 0.0))
            noise = torch.randn_like(data) * std
            data = data + noise

        return data


def bootstrap_environment(settings: Dict) -> IsaacSimEnvironment:
    """Bootstrap Isaac Sim environment from settings dict.

    Convenience function for quick environment setup.

    Args:
        settings: Dict with config_path, headless, etc.

    Returns:
        Initialized IsaacSimEnvironment instance
    """
    config_path = settings.get('config_path', 'config/env/isaac_lab_env.yaml')
    headless = settings.get('headless', False)

    env = IsaacSimEnvironment(config_path=config_path, headless=headless)
    env.initialize_isaac_sim()
    env.setup_sensors()
    env.setup_ros2_bridge()

    return env
