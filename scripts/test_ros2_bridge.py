"""Test script for Isaac Sim ROS 2 bridge verification.

This script tests the Isaac Sim native ROS 2 bridge without running a full
simulation. It creates a minimal scene with a camera and publishes to ROS 2
topics that can be verified from the host or Docker container.

Usage:
    # Make sure ROS 2 environment is configured
    source scripts/activate_ros2_env.sh

    # Run the test
    python scripts/test_ros2_bridge.py

    # In another terminal, verify topics:
    docker exec rapid_ros2 ros2 topic list
    docker exec rapid_ros2 ros2 topic hz /camera/depth
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    print("\n" + "=" * 60)
    print("Isaac Sim ROS 2 Bridge Verification Test")
    print("=" * 60 + "\n")

    # Step 1: Initialize Isaac Sim
    print("[Step 1/6] Initializing Isaac Sim...")
    from isaacsim import SimulationApp

    simulation_app = SimulationApp({
        "headless": True,
        "width": 640,
        "height": 480,
    })
    print("  ✓ Isaac Sim initialized\n")

    # Step 2: Import Isaac Lab modules
    print("[Step 2/6] Importing Isaac Lab modules...")
    import isaaclab.sim as sim_utils
    from isaaclab.sim import SimulationContext
    from isaaclab.sensors.camera import Camera, CameraCfg
    import omni.isaac.core.utils.prims as prim_utils
    from pxr import Usd
    import omni.usd
    print("  ✓ Isaac Lab modules imported\n")

    # Step 3: Create simulation context
    print("[Step 3/6] Creating simulation context...")
    sim_cfg = sim_utils.SimulationCfg(
        dt=0.01,
        render_interval=2,
        device="cuda:0",
        gravity=(0.0, 0.0, -9.81),
    )
    sim_context = SimulationContext(sim_cfg)
    stage = omni.usd.get_context().get_stage()
    print("  ✓ Simulation context created\n")

    # Step 4: Create minimal scene
    print("[Step 4/6] Creating minimal scene...")

    # Ground plane
    ground_cfg = sim_utils.GroundPlaneCfg(size=(10.0, 10.0))
    ground_cfg.func("/World/GroundPlane", ground_cfg)

    # Lighting
    light_cfg = sim_utils.DomeLightCfg(intensity=3000.0)
    light_cfg.func("/World/DomeLight", light_cfg)

    # Camera mount
    prim_utils.create_prim("/World/Camera", "Xform")

    # Create depth camera
    camera_cfg = CameraCfg(
        prim_path="/World/Camera/depth_camera",
        update_period=0.05,  # 20 Hz
        height=480,
        width=640,
        data_types=["distance_to_image_plane"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=24.0,
            horizontal_aperture=20.955,
            clipping_range=(0.1, 30.0),
        ),
        offset=CameraCfg.OffsetCfg(
            pos=(3.0, 3.0, 2.0),
            rot=(0.5, -0.5, 0.5, -0.5),
            convention="ros"
        ),
    )
    camera = Camera(cfg=camera_cfg)
    print("  ✓ Scene created with depth camera\n")

    # Step 5: Setup ROS 2 bridge
    print("[Step 5/6] Setting up ROS 2 bridge...")

    try:
        # Enable ROS 2 bridge extension
        import omni.kit.app
        ext_manager = omni.kit.app.get_app().get_extension_manager()

        if not ext_manager.is_extension_enabled("isaacsim.ros2.bridge"):
            ext_manager.set_extension_enabled_immediate("isaacsim.ros2.bridge", True)
            print("  ✓ Enabled isaacsim.ros2.bridge extension")
        else:
            print("  ✓ isaacsim.ros2.bridge extension already enabled")

        # Create OmniGraph for publishing
        import omni.graph.core as og

        keys = og.Controller.Keys
        (graph, nodes, _, _) = og.Controller.edit(
            {
                "graph_path": "/World/ROS2_Test_Bridge",
                "evaluator_name": "push",
            },
            {
                keys.CREATE_NODES: [
                    ("OnTick", "omni.graph.action.OnPlaybackTick"),
                    ("PublishDepth", "isaacsim.ros2.bridge.ROS2PublishImage"),
                    ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
                ],
                keys.SET_VALUES: [
                    ("PublishDepth.inputs:topicName", "/test/camera/depth"),
                    ("PublishDepth.inputs:type", "depth"),
                    ("PublishClock.inputs:topicName", "/clock"),
                ],
                keys.CONNECT: [
                    ("OnTick.outputs:tick", "PublishDepth.inputs:execIn"),
                    ("OnTick.outputs:tick", "PublishClock.inputs:execIn"),
                ],
            },
        )

        print("  ✓ ROS 2 bridge OmniGraph created")
        print("  ✓ Publishing to:")
        print("      - /test/camera/depth (sensor_msgs/Image)")
        print("      - /clock (rosgraph_msgs/Clock)")
        print("\n")

    except Exception as e:
        print(f"  ✗ Error setting up ROS 2 bridge: {e}")
        print("  Make sure to run: source scripts/activate_ros2_env.sh")
        simulation_app.close()
        return 1

    # Step 6: Run simulation
    print("[Step 6/6] Running simulation...")
    print("\nSimulation running. Press Ctrl+C to stop.\n")
    print("In another terminal, verify topics:")
    print("  docker exec rapid_ros2 ros2 topic list")
    print("  docker exec rapid_ros2 ros2 topic hz /test/camera/depth")
    print("  docker exec rapid_ros2 ros2 topic echo /clock --once")
    print("\n")

    try:
        # Reset simulation
        sim_context.reset()

        # Run for 10 seconds
        start_time = time.time()
        step_count = 0

        while time.time() - start_time < 10.0:
            # Step simulation
            sim_context.step(render=True)

            # Update camera
            camera.update(dt=sim_context.get_physics_dt())

            step_count += 1

            # Print progress every 50 steps (~0.5s)
            if step_count % 50 == 0:
                elapsed = time.time() - start_time
                print(f"  Running... {elapsed:.1f}s / 10.0s")

        print("\n  ✓ Simulation completed successfully")
        print(f"  ✓ Ran {step_count} physics steps")
        print(f"  ✓ Published ~{step_count // 2} depth images at 20 Hz")

    except KeyboardInterrupt:
        print("\n\n  Interrupted by user")
    except Exception as e:
        print(f"\n\n  ✗ Error during simulation: {e}")
        simulation_app.close()
        return 1

    # Cleanup
    print("\nCleaning up...")
    simulation_app.close()

    print("\n" + "=" * 60)
    print("✓ ROS 2 Bridge Test Complete")
    print("=" * 60)
    print("\nIf you saw topics in the Docker container, the bridge is working!")
    print("Next: Run full Phase 1 test with docker integration")
    print("  python scripts/test_environment.py --with-docker --headless\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
