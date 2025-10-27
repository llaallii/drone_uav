# TODO - Environment Configuration

## Phase 1 - Isaac Lab Setup

### Installation Documentation
- [x] Record Isaac Sim 5.0.0 installation steps (documented in `setup_instructions.md`)
- [x] Document Python 3.11 requirement
- [x] Document PyTorch + CUDA 12.8 installation
- [x] Create `isaac_lab_env.yaml` with version pinning
- [x] Create comprehensive `setup_instructions.md`

### ROS 2 Installation
- [ ] Install ROS 2 Humble for Windows
  - [ ] Download ROS 2 Humble binary release
  - [ ] Extract to `C:\dev\ros2_humble\` (or preferred location)
  - [ ] Create `setup_ros2.bat` activation script
  - [ ] Install `colcon-common-extensions` via pip
  - [ ] Verify installation: `ros2 --version`
  - [ ] Test topic tools: `ros2 topic list`

### Isaac Sim ROS 2 Bridge
- [ ] Verify Isaac Sim ROS 2 bridge availability
- [ ] Test bridge initialization from Python
- [ ] Document any Windows-specific bridge configuration
- [ ] Create bridge launch script/configuration

### Environment Activation
- [ ] Create `activate_env.bat` convenience script
  - [ ] Activates conda environment (env_isaaclab)
  - [ ] Loads ROS 2 environment
  - [ ] Sets RAPID_ROOT environment variable
  - [ ] Runs verification checks
- [ ] Test activation script on fresh terminal

### Sensor Configuration
- [x] Create `sensors.yaml` with all Phase 1 sensors
- [ ] Validate sensor parameters match Isaac Sim capabilities
- [ ] Test sensor configs with Isaac Sim
- [ ] Document any sensor limitations discovered

### Scene Configuration
- [x] Create `scenes_config.yaml` with 10 scene families
- [ ] Identify Isaac assets available for each scene family
- [ ] Document custom assets needed (if any)
- [ ] Test procedural generation parameters
- [ ] Validate randomization ranges

### Host Dependencies
- [ ] Document GPU requirements (NVIDIA RTX/Tesla, CUDA 12.8)
- [ ] Document VRAM requirements (8GB min, 16GB recommended)
- [ ] Document RAM requirements (16GB min, 32GB recommended)
- [ ] Document disk space requirements (50GB+)
- [ ] List any additional Windows-specific dependencies

### Verification
- [ ] Run full environment verification via `scripts/setup_sim.py`
- [ ] Verify all config files load without errors
- [ ] Test Isaac Sim GUI launch
- [ ] Test Isaac Sim headless launch
- [ ] Verify sensor creation from configs
- [ ] Verify scene loading from configs

## Phase 2+ - Future Configuration
- [ ] Planner parameter tuning configs
- [ ] Controller gain configs
- [ ] Disturbance model configs (wind, sensor noise variations)

## Notes
- All configuration files use YAML format for readability
- Windows paths use backslash notation (`.\data\`)
- Version pinning critical for reproducibility
- Document all deviations from original Linux-based plan
