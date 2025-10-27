# TODO - ROS 2 Configuration (Jazzy)

## Phase 1 - ROS 2 Bridge Setup

### Topic Specification
- [x] Enumerate required topics (`/depth`, `/odom`, `/imu`) with message types
- [x] Create `bridge_topics.yaml` with complete topic configuration
- [x] Define QoS settings for each topic
- [x] Specify TF tree structure (world → base_link → sensor frames)
- [x] Configure /clock topic for sim time synchronization

### Bridge Implementation
- [ ] Test Isaac Sim ROS 2 bridge initialization
- [ ] Verify bridge supports all required message types
  - [ ] `sensor_msgs/Image` (depth camera)
  - [ ] `sensor_msgs/CameraInfo` (camera calibration)
  - [ ] `sensor_msgs/Imu` (IMU data)
  - [ ] `nav_msgs/Odometry` (odometry)
  - [ ] `tf2_msgs/TFMessage` (transforms)
  - [ ] `rosgraph_msgs/Clock` (simulation time)
- [ ] Create bridge initialization code in `src/sim/environment.py`
- [ ] Test topic publication rates (target 20 Hz for sensors)
- [ ] Verify message contents and formats

### Launch Configuration
- [ ] Create `isaac_bridge_launch.py` ROS 2 launch file
  - [ ] Load bridge configuration from `bridge_topics.yaml`
  - [ ] Set up ROS_DOMAIN_ID (default: 0)
  - [ ] Configure use_sim_time parameter
  - [ ] Start bridge node
  - [ ] Start static TF publishers for sensor mounts
- [ ] Test launch file execution
- [ ] Document launch file usage in `setup_instructions.md`

### Topic Validation
- [ ] Create validation script to check all topics
- [ ] Use `ros2 topic list` to verify topics exist
- [ ] Use `ros2 topic info` to verify message types
- [ ] Use `ros2 topic hz` to measure publication rates
- [ ] Use `ros2 topic echo` to inspect message contents
- [ ] Verify TF tree with `ros2 run tf2_tools view_frames.py`

### Diagnostics
- [ ] Enable `/diagnostics` topic for bridge health monitoring
- [ ] Set up diagnostics publishing (1 Hz)
- [ ] Create diagnostics visualization/logging

### Integration Testing
- [ ] Test bridge with Isaac Sim in GUI mode
- [ ] Test bridge with Isaac Sim in headless mode
- [ ] Test bridge startup/shutdown robustness
- [ ] Test bridge behavior under high sensor rates
- [ ] Measure bridge latency (sensor reading → ROS 2 publish)

## Phase 2 - Planner Integration Topics
- [ ] Add subscriber topics for planner
  - [ ] `/trajectory` (nav_msgs/Path) - planned trajectory
  - [ ] `/occupancy_grid` or ESDF map topic
- [ ] Configure bi-directional bridge (publish + subscribe)

## Phase 3 - Controller Integration Topics
- [ ] Add control command subscriber
  - [ ] `/cmd_vel` (geometry_msgs/Twist) - velocity commands
- [ ] Test control loop latency (command → actuation)

## Future Enhancements
- [ ] Multi-drone namespace support (for swarm scenarios)
- [ ] Compressed image transport for depth images
- [ ] Rosbag recording integration for episodes

## Notes
- **Platform Update:** ROS 2 Jazzy on Ubuntu 24.04 LTS (native support)
- All sensor topics use reliable QoS (critical data)
- /clock topic uses best_effort QoS (standard practice)
- TF tree published at 20 Hz to match sensor rate
- Bridge runs in same process as Isaac Sim for low latency
- ROS 2 Jazzy provides improved performance and newer features compared to Humble
