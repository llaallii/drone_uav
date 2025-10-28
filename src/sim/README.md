# Isaac Lab Environment Wrapper - Phase 1 Implementation

This directory contains the Isaac Lab environment wrapper for RAPID v2, providing a unified interface for simulation, sensor management, and ROS 2 integration.

## Overview

The `environment.py` module implements the core simulation environment wrapper following Isaac Lab best practices and the Phase 1 requirements from CLAUDE.md.

### Key Features

✅ **Fully Implemented (Phase 1)**:
- Isaac Sim application initialization with proper sequence
- Depth camera sensor (640x480, 20 Hz, 0.1-30m range)
- IMU sensor (100 Hz internal, 20 Hz logging)
- Ground truth odometry (20 Hz)
- ROS 2 bridge with configurable QoS
- Scene management (basic ground plane + lighting)
- Simulation control (reset, step, close)
- Configuration-driven design (all parameters from YAML)

🚧 **Future Phases**:
- Procedural scene generation with Isaac Replicator (Phase 2)
- Drone robot integration (Phase 2-3)
- Data logging to Parquet (Phase 4)
- Quality control metrics (Phase 5)

## Architecture

### Initialization Sequence

**CRITICAL**: Isaac Sim requires a specific initialization order:

```python
1. Create SimulationApp FIRST
   └─> from isaacsim import SimulationApp
   └─> app = SimulationApp({"headless": True})

2. THEN import Isaac Lab modules
   └─> import isaaclab.sim as sim_utils
   └─> from isaaclab.sensors.camera import Camera

3. Create World and configure physics
   └─> world = SimulationContext(SimulationCfg(...))

4. Setup sensors and ROS 2 bridge
   └─> Sensors, bridge, scene loading
```

This order is enforced in the `IsaacSimEnvironment` class.

### Configuration Files

All simulation parameters are loaded from YAML files:

- **`config/env/isaac_lab_env.yaml`**: Physics timestep (100 Hz), rendering (20 Hz), device settings
- **`config/env/sensors.yaml`**: Sensor specifications, noise models, mount positions
- **`config/ros2/bridge_topics.yaml`**: ROS 2 topics, message types, QoS profiles

## Usage

### Basic Example

```python
from src.sim.environment import IsaacSimEnvironment

# Create environment
env = IsaacSimEnvironment(
    config_path="config/env/isaac_lab_env.yaml",
    headless=True  # Run without GUI
)

# Initialize Isaac Sim (must be called first!)
env.initialize_isaac_sim()

# Setup sensors and ROS 2 bridge
env.setup_sensors()
env.setup_ros2_bridge()

# Reset environment and load scene
obs = env.reset(scene_family="office", seed=42)

# Run simulation loop
for step in range(1000):
    obs = env.step()

    # Access sensor data
    depth_image = obs.get('depth')
    imu_accel = obs.get('imu_accel')
    imu_gyro = obs.get('imu_gyro')
    odom_pos = obs.get('odom_pos')

    # Your control logic here
    pass

# Cleanup
env.close()
```

### Using the Test Script

We provide a comprehensive test script to validate the implementation:

```bash
# Activate environment
conda activate env_isaaclab
source /opt/ros/jazzy/setup.bash

# Run test (headless mode, 100 steps)
python scripts/test_environment.py --headless --num_steps 100

# Run with GUI
python scripts/test_environment.py --num_steps 100

# Custom scene
python scripts/test_environment.py --scene_family warehouse --scene_seed 123
```

The test script validates:
- ✓ Environment initialization
- ✓ Isaac Sim application startup
- ✓ Sensor creation and configuration
- ✓ ROS 2 bridge setup
- ✓ Scene loading
- ✓ Simulation step execution
- ✓ Observation data collection

## API Reference

### `IsaacSimEnvironment`

Main environment class managing simulation lifecycle.

#### Constructor

```python
IsaacSimEnvironment(
    config_path: str = "config/env/isaac_lab_env.yaml",
    headless: bool = False
)
```

**Parameters**:
- `config_path`: Path to environment configuration YAML
- `headless`: Run in headless mode (no GUI)

#### Methods

##### `initialize_isaac_sim()`

Initialize Isaac Sim application context. **Must be called first** before any Isaac Lab operations.

**Returns**: `SimulationContext` instance

**Example**:
```python
env = IsaacSimEnvironment(headless=True)
world = env.initialize_isaac_sim()
```

---

##### `setup_sensors()`

Setup sensors from configuration (depth camera, IMU, odometry).

**Returns**: Dictionary of sensor instances

**Sensors Created**:
- `depth`: Camera sensor (640x480, 20 Hz, depth only)
- `imu`: IMU sensor (100 Hz internal rate)
- `odom`: Ground truth odometry (20 Hz)

**Example**:
```python
sensors = env.setup_sensors()
print(f"Active sensors: {list(sensors.keys())}")
```

---

##### `setup_ros2_bridge()`

Setup ROS 2 bridge with publishers for sensor topics.

**Returns**: ROS 2 bridge node instance (or None if ROS 2 unavailable)

**Topics Published**:
- `/camera/depth` (sensor_msgs/Image)
- `/camera/depth/camera_info` (sensor_msgs/CameraInfo)
- `/imu/data` (sensor_msgs/Imu)
- `/odom` (nav_msgs/Odometry)
- `/drone/state` (geometry_msgs/PoseStamped)
- `/clock` (rosgraph_msgs/Clock)

**Example**:
```python
bridge = env.setup_ros2_bridge()
if bridge:
    print("ROS 2 bridge active")
else:
    print("Running without ROS 2")
```

---

##### `load_scene(scene_family, seed, from_cache=True)`

Load or generate a scene.

**Parameters**:
- `scene_family` (str): Scene family (office, warehouse, forest, etc.)
- `seed` (int): Random seed for reproducibility
- `from_cache` (bool): Load from USD cache if available

**Returns**: Scene path string

**Note**: Phase 1 creates a basic ground plane. Procedural generation in Phase 2+.

**Example**:
```python
scene_path = env.load_scene("office", seed=42)
```

---

##### `reset(scene_family=None, seed=None)`

Reset simulation environment.

**Parameters**:
- `scene_family` (str, optional): New scene family to load
- `seed` (int, optional): New scene seed

**Returns**: Initial observation dictionary

**Example**:
```python
obs = env.reset(scene_family="warehouse", seed=123)
print(f"Initial observation keys: {obs.keys()}")
```

---

##### `step()`

Step simulation forward by one physics timestep.

**Returns**: Observation dictionary containing:
- `timestamp`: Simulation time (float)
- `depth`: Depth image tensor (H, W) if available
- `imu_accel`: Linear acceleration (3,) if available
- `imu_gyro`: Angular velocity (3,) if available
- `odom_pos`: Position (3,) if available
- `odom_vel`: Linear velocity (3,) if available
- `odom_quat`: Orientation quaternion (4,) if available

**Example**:
```python
for step_num in range(1000):
    obs = env.step()
    if 'depth' in obs:
        print(f"Depth image shape: {obs['depth'].shape}")
```

---

##### `close()`

Shutdown simulation environment gracefully.

Performs cleanup:
- Flushes data logger buffers
- Destroys ROS 2 bridge node
- Closes Isaac Sim application

**Example**:
```python
env.close()
```

---

### Helper Methods

These methods are used internally but can be accessed if needed:

##### `_get_sensor_observations()`

Collect all sensor data into observation dictionary.

**Returns**: Dictionary with sensor data

---

##### `_publish_ros2_messages(obs)`

Publish sensor observations to ROS 2 topics.

**Parameters**:
- `obs` (dict): Observation dictionary from `_get_sensor_observations()`

---

##### `_add_sensor_noise(data, noise_config)`

Add physics-based noise to sensor data.

**Parameters**:
- `data` (tensor): Sensor data tensor
- `noise_config` (dict): Noise configuration from sensors.yaml

**Returns**: Noisy sensor data

## Testing

### Test Script Validation

The test script (`scripts/test_environment.py`) performs comprehensive validation:

```bash
python scripts/test_environment.py --headless --num_steps 100
```

**Validation Phases**:
1. ✓ Environment object creation
2. ✓ Isaac Sim initialization
3. ✓ Sensor setup (depth, IMU, odometry)
4. ✓ ROS 2 bridge setup
5. ✓ Environment reset with scene loading
6. ✓ Simulation loop (100 steps)

**Expected Output**:
```
================================================================================
Isaac Lab Environment Wrapper - Test Script
================================================================================
[Phase 1/6] Creating IsaacSimEnvironment...
  ✓ Environment object created successfully
[Phase 2/6] Initializing Isaac Sim application...
  ✓ Isaac Sim initialized successfully
[Phase 3/6] Setting up sensors...
  ✓ Sensors configured successfully
  ✓ Active sensors: ['depth', 'imu', 'odom']
[Phase 4/6] Setting up ROS 2 bridge...
  ✓ ROS 2 bridge initialized successfully
[Phase 5/6] Resetting environment...
  ✓ Environment reset successfully
[Phase 6/6] Running simulation for 100 steps...
  ✓ Simulation completed successfully (100 steps)
[Cleanup] Closing environment...
  ✓ Environment closed successfully
================================================================================
✓ Test completed successfully!
================================================================================
```

### Manual Testing

You can also test individual components:

```python
# Test sensor creation only
env = IsaacSimEnvironment(headless=True)
env.initialize_isaac_sim()
sensors = env.setup_sensors()
print(f"Sensors: {list(sensors.keys())}")
env.close()

# Test ROS 2 bridge only
env = IsaacSimEnvironment(headless=True)
env.initialize_isaac_sim()
bridge = env.setup_ros2_bridge()
if bridge:
    print(f"Publishers: {list(bridge.publishers.keys())}")
env.close()
```

## Troubleshooting

### Common Issues

#### "No module named 'isaacsim'"

**Solution**: Ensure Isaac Sim is installed and environment is activated:
```bash
conda activate env_isaaclab
pip show isaacsim  # Should show version 5.0.0.x
```

#### "ROS 2 (rclpy) not available"

**Solution**: Source ROS 2 setup:
```bash
source /opt/ros/jazzy/setup.bash
python -c "import rclpy; print('ROS 2 available')"
```

The environment will run without ROS 2 if not available (warning printed).

#### "CUDA not available"

**Solution**: Verify PyTorch CUDA installation:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Reinstall PyTorch with CUDA 12.8 if needed:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

#### Sensor data is None

**Cause**: Sensors need to be updated before reading data.

**Solution**: Call `env.step()` at least once before accessing sensor observations:
```python
env.reset()
obs = env.step()  # First step populates sensor data
print(obs['depth'])  # Now contains data
```

## Implementation Notes

### Phase 1 Limitations

The current implementation provides a working foundation with some Phase 1 simplifications:

1. **Scene Generation**: Uses basic ground plane + lighting. Procedural generation (10 scene families with Isaac Replicator) will be added in Phase 2.

2. **Drone Robot**: Uses placeholder prims. Actual quadrotor articulation with motors and dynamics will be added in Phase 2-3.

3. **Odometry**: Ground truth from simulation. Estimated odometry from sensor fusion will be added in Phase 2.

4. **Data Logging**: Placeholder for logger. Full logging to Parquet with QC will be added in Phase 4-5.

5. **ROS 2 Publishing**: Publishers created but message conversion not fully implemented. Will be completed with actual robot integration.

### Configuration-Driven Design

All parameters come from YAML files, never hardcoded:
- Sensor rates, resolutions, noise parameters
- ROS 2 topics, QoS settings
- Physics/rendering timesteps
- Scene generation parameters

This makes it easy to reconfigure without code changes.

### Sensor Coordinate Frames

All sensors use **ROS convention** (x-forward, z-up):
- Depth camera: 10 cm forward from drone center
- IMU: At drone center of mass
- Odometry: Drone body frame

TF tree: `world → base_link → sensor_frames`

## Next Steps (Phase 2+)

The environment wrapper is ready for Phase 2 enhancements:

1. **Scene Generation Module**: Create `src/sim/scene_generator.py` with Isaac Replicator integration
2. **Drone Robot**: Add quadrotor URDF/USD with motors and physics
3. **Fast-Planner Integration**: Connect planner to environment in `src/planning/`
4. **Controller**: Geometric attitude controller at 50 Hz in `src/control/`
5. **Data Pipeline**: Logging to Parquet with QC in `tools/logging_utils.py`

## References

- [Isaac Lab Documentation](https://isaac-sim.github.io/IsaacLab/main/)
- [RAPID v2 Plan](../../docs/plan.md)
- [Phase 1 Checklist](../../docs/phase1_checklist.md)
- [Sensor Configuration](../../config/env/sensors.yaml)
- [ROS 2 Bridge Configuration](../../config/ros2/bridge_topics.yaml)
