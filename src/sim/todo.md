# TODO - Simulation Module

## Phase 1 - Environment Setup

### Environment Wrapper (`environment.py`)
- [x] Create file with basic structure
- [ ] Implement `IsaacSimEnvironment` class
  - [ ] Initialize Isaac Sim application context
  - [ ] Load scene from USD file or procedurally generate
  - [ ] Configure physics settings (dt=0.01, rendering dt=0.05)
  - [ ] Set up camera viewport for headless/GUI modes
- [ ] Implement `setup_sensors()` method
  - [ ] Load sensor config from `config/env/sensors.yaml`
  - [ ] Create stereo depth camera with noise model
  - [ ] Create IMU sensor (100 Hz internal, 20 Hz logging)
  - [ ] Create ground truth odometry sensor
  - [ ] Configure sensor mounts (positions/orientations)
- [ ] Implement `setup_ros2_bridge()` method
  - [ ] Load bridge config from `config/ros2/bridge_topics.yaml`
  - [ ] Initialize ROS 2 bridge node
  - [ ] Register sensor topics (`/camera/depth`, `/imu/data`, `/odom`)
  - [ ] Set up TF tree publisher (world → base_link → sensor frames)
  - [ ] Configure QoS settings per topic
- [ ] Implement `reset()` method
  - [ ] Reset simulation state
  - [ ] Randomize drone initial pose
  - [ ] Clear sensor buffers
  - [ ] Reset ROS 2 timestamps
- [ ] Implement `step()` method
  - [ ] Advance physics simulation by one timestep
  - [ ] Update sensor readings
  - [ ] Publish ROS 2 messages
  - [ ] Return observation dict
- [ ] Implement `close()` method
  - [ ] Shutdown ROS 2 bridge gracefully
  - [ ] Close Isaac Sim application
  - [ ] Clean up resources

### Scene Management
- [ ] Create `scene_loader.py` module
  - [ ] Implement `load_scene_from_config(scene_family, seed)` function
  - [ ] Load scene config from `config/env/scenes_config.yaml`
  - [ ] Support USD scene loading from cache
  - [ ] Support procedural scene generation
  - [ ] Validate scene navigability (free space, path existence)
- [ ] Create `scene_generator.py` module
  - [ ] Implement procedural generation for 10 scene families
  - [ ] Use Isaac Sim Prim API for asset placement
  - [ ] Apply Isaac Replicator randomization (lighting, materials)
  - [ ] Log scene seeds to `.\data\raw\runtime\scenes.jsonl`
  - [ ] Cache generated scenes as USD files

### Drone/Robot Setup
- [ ] Create `drone_model.py` module
  - [ ] Define quadrotor robot using Isaac Sim ArticulationRoot
  - [ ] Configure mass, inertia tensor, motor properties
  - [ ] Set up collision geometry
  - [ ] Implement motor dynamics (±15% gain randomization, τ=0.02s lag)
  - [ ] Expose control interface for Phase 3

### Randomization
- [ ] Create `randomization.py` module
  - [ ] Implement lighting randomization (intensity, color temp, HDR)
  - [ ] Implement material randomization (albedo, roughness, metallic)
  - [ ] Implement dynamic obstacle placement (disabled in Phase 1)
  - [ ] Implement environmental effects (fog, wind - Phase 6+)
  - [ ] Integrate with Isaac Replicator API

### Logging & Data Collection
- [ ] Create `data_logger.py` module
  - [ ] Implement sensor data logging to `.\data\raw\runtime\sensors\`
  - [ ] Log depth images (LZ4 compression)
  - [ ] Log IMU data (downsampled to 20 Hz)
  - [ ] Log odometry data
  - [ ] Include timestamps, sensor configs, simulation params
  - [ ] Implement flush mechanism (buffer 100MB, flush every 5s)

## Phase 2 - Planner Integration
- [ ] Add planner state subscriber (for Fast-Planner integration)
- [ ] Implement trajectory visualization in Isaac Sim viewport
- [ ] Add occupancy map publisher for ESDF generation

## Phase 3 - Controller Integration
- [ ] Implement control command subscriber (`/cmd_vel`)
- [ ] Apply motor dynamics and actuation lag
- [ ] Add disturbance models (wind, mass/inertia variation)

## Testing
- [ ] Unit test for environment initialization
- [ ] Unit test for sensor configuration loading
- [ ] Unit test for ROS 2 bridge topic publishing
- [ ] Integration test for full simulation loop
- [ ] Validation test for scene generation

## Documentation
- [ ] Add docstrings to all public methods
- [ ] Create usage examples in `src/sim/examples/`
- [ ] Document Isaac Sim API usage patterns
