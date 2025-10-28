# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAPID v2 is an end-to-end autonomous drone learning pipeline built on Isaac Lab/Isaac Sim 5.0.0. The project progresses through 11 phases: from environment setup (Phase 1), through expert trajectory generation with Fast-Planner (Phase 2-3), dataset curation (Phase 4-6), sim-to-real alignment (Phase 7), to inverse reinforcement learning and continuous learning loops (Phase 9-11).

**Current Status**: Phase 1 (Environment Setup) - Implementing Isaac Lab foundation, procedural scene generation, and ROS 2 Jazzy bridge integration.

## Environment Setup

### Critical Activation Sequence
```bash
# Always run these commands before working with the codebase
conda activate env_isaaclab
source /opt/ros/jazzy/setup.bash
```

### Platform Requirements
- **OS**: Ubuntu 24.04 LTS (Noble Numbat)
- **Python**: 3.11 (in conda environment `env_isaaclab`)
- **Isaac Sim**: 5.0.0 (installed via pip)
- **PyTorch**: 2.7.0 with CUDA 12.8
- **ROS 2**: Jazzy (native to Ubuntu 24.04)

### Verification
```bash
# Verify entire Phase 1 environment setup
python scripts/setup_sim.py

# Verify individual components
pip show isaacsim              # Should show version 5.0.0.x
ros2 --version                 # Should show "jazzy"
python -c "import torch; print(torch.cuda.is_available())"  # Should be True
```

## Architecture Patterns

### Configuration-Driven Design
All simulation parameters, sensors, and ROS 2 topics are defined declaratively in YAML files under `config/`:
- [config/env/isaac_lab_env.yaml](config/env/isaac_lab_env.yaml) - Isaac Sim and environment settings
- [config/env/sensors.yaml](config/env/sensors.yaml) - Sensor specs (20Hz depth, IMU, odometry)
- [config/env/scenes_config.yaml](config/env/scenes_config.yaml) - 10 scene families with procedural generation
- [config/ros2/bridge_topics.yaml](config/ros2/bridge_topics.yaml) - ROS 2 topic mappings and QoS settings

When implementing features, load parameters from these configs rather than hardcoding values.

### Phase-Based Development
The codebase follows an 11-phase roadmap (see [docs/plan.md](docs/plan.md)). Most modules contain skeleton implementations with `TODO Phase N:` comments indicating when features should be developed.

**Active Phase 1 deliverables**:
- Isaac Lab environment wrapper in [src/sim/environment.py](src/sim/environment.py)
- Scene generation scripts (to be created in `scripts/`)
- ROS 2 bridge integration and testing

**Future phases** include planner integration (Phase 2), controller (Phase 3), data logging (Phase 4-6), IRL training (Phase 9-11).

### Isaac Sim Initialization Order
When working with Isaac Sim code, follow this strict initialization sequence:

1. Import and create `SimulationApp` first (with headless flag)
2. Import Isaac Lab modules only after `SimulationApp` is created
3. Load scenes before setting up sensors
4. Start ROS 2 bridge last

Example:
```python
from isaacsim import SimulationApp
app = SimulationApp({"headless": headless})

# Only import Isaac Lab after SimulationApp exists
import omni.isaac.lab
# ... rest of initialization
```

### Module Organization
- `src/sim/` - Isaac Sim environment wrapper, scene loading
- `src/planning/` - Split into `global/`, `local/`, `mapping/` (Fast-Planner integration in Phase 2)
- `src/control/` - Geometric controller (50Hz, Phase 3)
- `src/analysis/` - Trajectory metrics (jerk, clearance, feasibility)
- `tools/` - Utilities like logging helpers
- `data/` - Runtime logs, processed datasets, QC reports

### Scene Generation Pattern
Scenes use procedural generation with seed-based reproducibility:
- 10 scene families: Office, Warehouse, Forest, Urban, Cave, Maze, Mine, Shipyard, Ruins, Jungle
- Seeds logged to `data/raw/runtime/scenes.jsonl` for reproducibility
- Isaac Replicator randomizes lighting, materials, object placement
- Cached as USD files in `data/raw/scenes/cache/`

### Sensor and ROS 2 Integration
All sensors operate at 20Hz with physics-based noise models:
- Depth camera: `/camera/depth` (sensor_msgs/Image, 32FC1)
- IMU: `/imu/data` (sensor_msgs/Imu, 100Hz internal → 20Hz logged)
- Odometry: `/odom` (nav_msgs/Odometry, ground truth in Phase 1)

ROS 2 bridge configuration uses declarative YAML with proper QoS:
- `reliability: reliable` for control topics
- `durability: volatile` for sensor streams
- `use_sim_time: true` for synchronized timestamps

### Data Pipeline Convention
- `data/raw/runtime/` - Live simulation logs, scene seeds
- `data/processed/` - Parquet shards for training (Phase 4+)
- `data/qc/` - Quality control scorecards (Phase 5+)
- `data/schema/` - Metadata and schema definitions

## Common Development Tasks

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_planning.py

# Run with verbose output
pytest -v tests/
```

### Implementing Phase 1 Components
The main implementation tasks for Phase 1 are in [src/sim/environment.py](src/sim/environment.py). Look for `TODO Phase 1:` comments marking methods that need implementation:
- `initialize_isaac_sim()` - Set up Isaac Sim application and physics
- `setup_sensors()` - Create depth camera, IMU, odometry from config
- `setup_ros2_bridge()` - Initialize ROS 2 node and publishers
- `load_scene()` - Load or generate procedural scenes
- `reset()` - Reset environment state
- `step()` - Advance simulation and collect sensor data

### Scene Generation Scripts
Create scene generation scripts in `scripts/` directory:
- Individual scene generation (load config, generate scene, save USD)
- Batch generation across all scene families
- Validation of scene navigability

## Important Implementation Notes

### Phase 2+ Planner Integration (Future)
- ESDF mapping from depth + odometry fusion
- Kinodynamic A* with B-spline trajectory smoothing
- Homotopy class enumeration for topological diversity
- Velocity limits: ≤30 m/s, acceleration: ≤10 m/s²
- 10Hz replanning rate

### Phase 3+ Controller Specifications (Future)
- Geometric attitude controller at 50Hz
- ±15% gain randomization for robustness
- Motor lag simulation: τ = 0.02s
- Dynamic disturbances: wind 0-5 m/s, mass/inertia ±10%

### Logging and Metrics
Use [tools/logging_utils.py](tools/logging_utils.py) for consistent data recording:
- Trajectory metrics: jerk, clearance, feasibility
- Episode logs stored as timestamped files
- QC scorecards follow data quality templates (Phase 5+)

## Documentation Structure

Key documentation files:
- [docs/plan.md](docs/plan.md) - Complete 11-phase roadmap with deliverables
- [docs/phase1_checklist.md](docs/phase1_checklist.md) - Phase 1 completion criteria
- [config/env/setup_instructions.md](config/env/setup_instructions.md) - Detailed environment setup
- [docs/owner_log.md](docs/owner_log.md) - Development decisions and platform migration notes
- [README.md](README.md) - Quick start and repository overview

Each subdirectory contains:
- `notes.md` - Design notes and architectural decisions
- `todo.md` - Outstanding tasks and implementation priorities

## File Naming Conventions
- Config files: snake_case with descriptive suffixes (`sensors.yaml`, `bridge_topics.yaml`)
- Python modules: snake_case following standard conventions
- Data files: Include timestamps and phase indicators
- Scripts: Action-oriented names (`setup_sim.py`, `run_planner.py`)
