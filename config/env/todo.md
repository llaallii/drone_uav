# TODO - Environment Configuration

## Phase 1 - Isaac Lab Setup

### Installation Documentation
- [x] Record Isaac Sim 5.0.0 installation steps (documented in `setup_instructions.md`)
- [x] Document Python 3.11 requirement
- [x] Document PyTorch + CUDA 12.8 installation
- [x] Create `isaac_lab_env.yaml` with version pinning
- [x] Create comprehensive `setup_instructions.md`

### ROS 2 Installation
- [x] Install ROS 2 Jazzy on Ubuntu 24.04 ✅
  - [x] Installed ROS 2 Jazzy desktop via apt ✅
  - [x] Configured environment in `~/.bashrc` ✅
  - [x] Installed `colcon-common-extensions` and `rosdep` ✅
  - [x] Verified installation: `ros2 --version` ✅
  - [x] Tested topic tools: `ros2 topic list` ✅

### Isaac Sim ROS 2 Bridge
- [ ] Verify Isaac Sim ROS 2 bridge availability with Jazzy
- [ ] Test bridge initialization from Python
- [ ] Document Ubuntu-specific bridge configuration
- [ ] Create bridge launch script/configuration

### Isaac Lab Installation
- [x] Isaac Lab cloned and installed ✅
- [x] Verified Isaac Lab accessibility in conda environment ✅
- [x] Tested Isaac Lab utilities and sensors ✅

### Environment Activation
- [ ] Create `activate_env.sh` convenience script
  - [ ] Activates conda environment (env_isaaclab)
  - [ ] Loads ROS 2 Jazzy environment
  - [ ] Sets RAPID_ROOT environment variable
  - [ ] Runs verification checks
- [ ] Make script executable and test on fresh terminal

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
- [x] Document GPU requirements (NVIDIA RTX/Tesla, CUDA 12.8) ✅
- [x] Document VRAM requirements (8GB min, 16GB recommended) ✅
- [x] Document RAM requirements (16GB min, 32GB recommended) ✅
- [x] Document disk space requirements (50GB+) ✅
- [x] Updated for Ubuntu 24.04 LTS platform ✅

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
- Ubuntu/Linux paths use forward slash notation (`./data/`)
- Version pinning critical for reproducibility
- Platform migrated from Windows to Ubuntu 24.04 LTS for better ROS 2 and Isaac Lab compatibility
- ROS 2 Jazzy is native to Ubuntu 24.04, providing better performance than Humble
