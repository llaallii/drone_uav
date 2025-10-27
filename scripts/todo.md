# TODO - Scripts

## Phase 1 - Environment Setup Scripts

### Setup & Verification
- [x] Create `setup_sim.py` stub
- [ ] Implement `setup_sim.py` — Environment verification script
  - [ ] Check Isaac Sim installation (`pip show isaacsim`)
  - [ ] Verify Python version (3.11)
  - [ ] Check CUDA availability (`torch.cuda.is_available()`)
  - [ ] Test Isaac Sim launch (`isaacsim --help`)
  - [ ] Verify ROS 2 installation (`ros2 --version`)
  - [ ] Check directory structure (`.\data\raw\runtime\`, etc.)
  - [ ] Validate config files exist (sensors.yaml, scenes_config.yaml, bridge_topics.yaml)
  - [ ] Test Isaac Sim basic scene load
  - [ ] Report setup status (pass/fail with actionable errors)

- [ ] Create `test_sensors.py` — Sensor validation script
  - [ ] Load sensor config from `config/env/sensors.yaml`
  - [ ] Initialize Isaac Sim with minimal scene
  - [ ] Create depth camera, IMU, odometry sensors
  - [ ] Verify sensor data shapes and ranges
  - [ ] Check sensor update rates (20 Hz target)
  - [ ] Test sensor noise models
  - [ ] Validate sensor mount positions
  - [ ] Generate sensor validation report

- [ ] Create `test_ros2_bridge.py` — ROS 2 bridge testing script
  - [ ] Load bridge config from `config/ros2/bridge_topics.yaml`
  - [ ] Initialize Isaac Sim with ROS 2 bridge
  - [ ] Verify bridge node is running
  - [ ] Check topic publication (`ros2 topic list`)
  - [ ] Subscribe to sensor topics and verify message types
  - [ ] Test TF tree publication
  - [ ] Measure topic rates and latency
  - [ ] Generate bridge validation report

### Scene Generation
- [ ] Create `generate_scenes.py` — Scene generation script
  - [ ] Load scenes config from `config/env/scenes_config.yaml`
  - [ ] Implement CLI: `--family [office|warehouse|...]`, `--count N`, `--seed S`
  - [ ] Generate scenes procedurally for selected family
  - [ ] Apply Isaac Replicator randomization
  - [ ] Validate scene navigability
  - [ ] Save scenes as USD files to cache
  - [ ] Log scene seeds to `.\data\raw\runtime\scenes.jsonl`
  - [ ] Generate preview images for visual inspection

- [ ] Create `batch_generate_scenes.py` — Batch scene generation
  - [ ] Generate all 10 scene families
  - [ ] 50 scenes per family (500 total)
  - [ ] Parallel generation if possible
  - [ ] Progress tracking and ETA
  - [ ] Error handling and retry logic
  - [ ] Final validation report

- [ ] Create `visualize_scene.py` — Scene visualization utility
  - [ ] Load scene from USD cache by seed
  - [ ] Launch Isaac Sim in GUI mode
  - [ ] Add camera controls for inspection
  - [ ] Display scene metadata (family, seed, assets)

### Data Management
- [ ] Create `setup_data_dirs.py` — Directory structure setup
  - [ ] Create `.\data\raw\runtime\`
  - [ ] Create `.\data\raw\runtime\sensors\`
  - [ ] Create `.\data\raw\scenes\cache\`
  - [ ] Create `.\data\dataset\shards\`
  - [ ] Set up logging directories for all 10 scene families

## Phase 2 - Planner Integration Scripts
- [x] Create `run_planner.py` stub
- [ ] Implement `run_planner.py` — Planner pipeline runner
  - [ ] Load scene and initialize environment
  - [ ] Start ROS 2 bridge
  - [ ] Launch planner nodes (mapping, global, local)
  - [ ] Visualize planned trajectories
  - [ ] Log planner metrics (jerk, clearance, feasibility)

## Phase 3+ - Future Scripts
- [ ] `run_controller_loop.py` — Controller-in-the-loop execution
- [ ] `collect_episode.py` — Record full expert trajectory episode
- [ ] `batch_collect.py` — Automated episode collection for dataset

## Utility Scripts
- [ ] `clean_logs.py` — Clean up runtime logs and temp files
- [ ] `validate_dataset.py` — Validate dataset integrity (Phase 4-5)
- [ ] `generate_qc_report.py` — Quality control report generation (Phase 5)

## Notes
- All scripts should use argparse for CLI arguments
- Include progress bars for long-running operations
- Generate actionable error messages with fix suggestions
- Log to console and optionally to file
- Support headless and GUI modes where applicable
