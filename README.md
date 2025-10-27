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

### Prerequisites
- **Isaac Sim 5.0.0:** Installed via pip in `env_isaaclab` conda environment (Python 3.11)
- **ROS 2 Humble:** Required for Windows (installation instructions in `config/env/setup_instructions.md`)
- **Windows Platform:** Development environment configured for Windows paths and workflows

### Quick Start
1. Activate the Isaac Lab environment:
   ```bash
   conda activate env_isaaclab
   ```

2. Verify Isaac Sim installation:
   ```bash
   isaacsim
   ```

3. Verify Phase 1 setup:
   ```bash
   python scripts/setup_sim.py
   ```

See `config/env/setup_instructions.md` for complete setup documentation.

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
**Phase 1 (ACTIVE):** Environment setup and configuration
- Isaac Sim 5.0.0 installed via pip in `env_isaaclab` environment
- Transitioning from original multi-repo Linux plan to Windows monorepo workflow
- Implementing Isaac Lab + ROS 2 Humble integration
- Configuring procedural scene generation with 10 scene families
- Setting up sensor pipeline (stereo depth, IMU, odometry) at 20 Hz

**Documentation Updates:**
- `docs/plan.md` &mdash; Updated Phase 1 for Isaac Lab approach
- `docs/phase1_checklist.md` &mdash; Phase 1 completion criteria
- `config/env/` &mdash; Environment manifests and sensor configurations
- `config/ros2/` &mdash; ROS 2 bridge specifications

## Next Steps
1. Install and configure ROS 2 Humble for Windows (see `config/env/todo.md`)
2. Implement Isaac Lab environment wrapper in `src/sim/environment.py`
3. Create scene generation scripts with randomization (10 families)
4. Verify ROS 2 bridge topics: `/depth`, `/odom`, `/imu`
5. Complete Phase 1 deliverables (see `docs/phase1_checklist.md`)

Track progress in `docs/owner_log.md` for decisions, assumptions, and blockers.
