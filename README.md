# RAPID v2 Drone Autonomy Sandbox

RAPID v2 is a single-operator effort to build an end-to-end autonomous drone pipeline: Isaac Lab environment setup, expert trajectory generation, dataset curation, inverse reinforcement learning, and sim-to-real deployment. The detailed eleven-phase roadmap lives in `docs/plan.md`.

## Roadmap Snapshot
- **Phase 1 (ACTIVE):** Isaac Lab foundation (Isaac Sim 5.0.0 via pip), reproducible scenes, ROS 2 Humble bridge, Windows workflow.
- **Phase 2:** Expert planner stack (mapping, kinodynamic global planner, 10 Hz replanner).
- **Phase 3-5:** Controller integration, logging, QC scorecards.
- **Phase 6-8:** Curriculum expansion, dataset freeze, release packaging.
- **Phase 9-11:** IRL training, sim-to-real fine-tuning, continuous learning loop.

Refer to `docs/plan.md` for full objectives, deliverables, and success criteria.

## Environment Setup

### Prerequisites ✅ COMPLETED
- **Operating System:** Ubuntu 24.04 LTS (Noble Numbat)
- **Isaac Sim 5.0.0:** Installed via pip in `env_isaaclab` conda environment (Python 3.11)
- **PyTorch 2.7.0:** With CUDA 12.8 support
- **ROS 2 Jazzy:** Native to Ubuntu 24.04 LTS
- **Isaac Lab:** Installed and integrated for robotics utilities and sensors

### Quick Start
1. Activate the Isaac Lab environment:
   ```bash
   conda activate env_isaaclab
   source /opt/ros/jazzy/setup.bash
   ```

2. Verify Isaac Sim installation:
   ```bash
   pip show isaacsim
   isaacsim --help
   ```

3. Verify ROS 2 Jazzy:
   ```bash
   ros2 --version
   echo $ROS_DISTRO
   ```

4. Run Phase 1 setup verification:
   ```bash
   python scripts/setup_sim.py
   ```

See [config/env/setup_instructions.md](config/env/setup_instructions.md) for complete setup documentation.

## Repository Layout
- `docs/` &mdash; Planning artifacts, owner notes, and phase tracking.
- `src/` &mdash; Python modules for simulation, planning, control, and analysis.
- `config/` &mdash; Environment and ROS 2 manifests, planner parameters, sensor configurations.
- `data/` &mdash; Raw logs, processed shards, QC reports, schema definitions.
- `tools/`, `scripts/` &mdash; Utility code and runnable automation entry points.
- `tests/` &mdash; Unit and integration tests growing with implementation.
- `infra/`, `experiments/` &mdash; CI scaffolding and experiment tracking space.

Each directory contains a `notes.md` describing its role in the pipeline and a `todo.md` with outstanding tasks.

## Current Status
**Phase 1 (ACTIVE):** Environment setup completed, implementation in progress

### Completed ✅
- **Platform Migration:** Successfully migrated to Ubuntu 24.04 LTS
- **Environment Setup:** Isaac Sim 5.0.0, Python 3.11, PyTorch 2.7.0, CUDA 12.8
- **ROS 2 Jazzy:** Installed and verified on Ubuntu 24.04
- **Isaac Lab:** Installed and integrated for sensors and robotics utilities
- **Configuration Files:** All YAML configs created
  - Environment manifests (`config/env/`)
  - Sensor configurations (`config/env/sensors.yaml`)
  - Scene families (`config/env/scenes_config.yaml`)
  - ROS 2 bridge specifications (`config/ros2/bridge_topics.yaml`)
- **Documentation:** Updated for Ubuntu 24.04 and ROS 2 Jazzy
  - [docs/plan.md](docs/plan.md) — Updated Phase 1 for Isaac Lab approach
  - [docs/phase1_checklist.md](docs/phase1_checklist.md) — Phase 1 completion criteria
  - [config/env/setup_instructions.md](config/env/setup_instructions.md) — Complete setup guide
  - [docs/owner_log.md](docs/owner_log.md) — Platform migration notes

### In Progress
- Isaac Lab environment wrapper implementation (`src/sim/environment.py`)
- Scene generation scripts with randomization (10 families)
- ROS 2 Jazzy bridge integration and testing

## Next Steps
1. Implement `IsaacSimEnvironment` class methods in `src/sim/environment.py`
2. Create scene generation scripts:
   - `scripts/generate_scenes.py` — Individual scene generation
   - `scripts/batch_generate_scenes.py` — Batch scene generation
3. Test ROS 2 Jazzy bridge with sensor topics: `/depth`, `/odom`, `/imu`
4. Generate and validate initial test scenes (10-20 across scene families)
5. Complete Phase 1 deliverables (see [docs/phase1_checklist.md](docs/phase1_checklist.md))

Track progress in [docs/owner_log.md](docs/owner_log.md) for decisions, assumptions, and blockers.
