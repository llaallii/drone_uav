# TODO - RAPID v2 Project

## Environment Setup (Phase 1) - MOSTLY COMPLETE ✅

### Completed
- [x] Platform migration from Windows to Ubuntu 24.04 LTS ✅
- [x] Isaac Sim 5.0.0 installation via pip in `env_isaaclab` ✅
- [x] Python 3.11 and PyTorch 2.7.0 with CUDA 12.8 ✅
- [x] ROS 2 Jazzy installation and configuration ✅
- [x] Isaac Lab installation and integration ✅
- [x] Configuration files created (env, sensors, scenes, ROS 2 bridge) ✅
- [x] Documentation updated for Ubuntu 24.04 and ROS 2 Jazzy ✅
- [x] Verification script implemented (`scripts/setup_sim.py`) ✅

### In Progress
- [ ] Implement Isaac Lab environment wrapper in `src/sim/environment.py`
- [ ] Create scene generation scripts
  - [ ] `scripts/generate_scenes.py` - Individual scene generation
  - [ ] `scripts/batch_generate_scenes.py` - Batch generation
  - [ ] `scripts/visualize_scene.py` - Scene inspection
- [ ] Test ROS 2 Jazzy bridge with Isaac Sim
- [ ] Validate sensor pipeline (depth, IMU, odometry)

### Next Steps
- [ ] Generate initial test scenes (10-20 across scene families)
- [ ] Complete ROS 2 bridge testing and validation
- [ ] Create environment activation script (`activate_env.sh`)
- [ ] Finalize Phase 1 deliverables

## Phase 2 Planning
- [ ] Review Fast-Planner integration requirements
- [ ] Define planner-controller interface specifications
- [ ] Plan mapping module architecture

## Documentation
- [x] Top-level README outlining eleven-phase roadmap ✅
- [x] Owner log with decisions and platform migration notes ✅
- [x] Phase 1 checklist with completion criteria ✅
- [x] Setup instructions for Ubuntu 24.04 ✅
