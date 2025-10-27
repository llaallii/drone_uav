# Owner Log

Central thread for decisions, assumptions, and follow-ups while executing the RAPID v2 roadmap as a solo project.

## Active Decisions
- **2025-10-27:** Phase 1 is now ACTIVE. Pivoting from deferred Phase 1 to immediate environment setup.
- **2025-10-27:** Using Isaac Lab framework (hybrid approach) instead of raw Isaac Sim for better sensor/ROS 2 integration and RL-ready infrastructure.
- **2025-10-27:** Adopting pip-based Isaac Sim 5.0.0 installation in `env_isaaclab` conda environment instead of binary installation at `/opt/NVIDIA/isaac_sim`.
- **2025-10-27:** Implementing Windows-compatible workflow with relative paths (`.\data\`) instead of Linux absolute paths (`/data/rapid_v2/`).
- **2025-10-27:** Using monorepo structure at current project root instead of multi-repo workspace (`~/rapid_v2_ws` with separate repos).
- **2025-10-27:** Targeting ROS 2 Humble for Windows compatibility.
- **2025-10-27:** Leveraging both Isaac Lab assets and custom procedural scene generation for 10 scene families.

## Assumptions
- Isaac Sim 5.0.0 remains stable; no breaking changes expected before Phase 1 completion.
- ROS 2 Humble on Windows will provide sufficient compatibility with Isaac Sim ROS 2 bridge.
- Isaac Lab's sensor framework (cameras, IMU, odometry) will meet Phase 1-2 requirements.
- Windows environment can support full simulation + ROS 2 + planning pipeline.
- Single-operator workflow means automation (scripts/tests) must offset lack of parallel work.
- Isaac Lab's abstractions won't conflict with Fast-Planner integration in Phase 2.
- Relative `.\data\` paths will work across development and deployment.

## Platform & Setup Notes
- **Operating System:** Windows (not Linux as originally planned)
- **Isaac Sim Version:** 5.0.0 (installed via pip, not binary)
- **Python Version:** 3.11 (in `env_isaaclab` conda environment)
- **Isaac Lab:** Using framework for sensors, robots, ROS 2 bridge, RL utilities
- **ROS 2 Distribution:** Humble (to be installed)
- **Workspace Structure:** Monorepo at `C:\Users\ratan\Desktop\drone_uav`

## Open Questions
- What are the specific performance characteristics of Isaac Lab vs raw Isaac Sim for our drone simulation needs?
- Will ROS 2 Humble on Windows have any latency/performance issues compared to Linux?
- Which Isaac Lab assets are suitable for our 10 scene families (Office, Warehouse, Forest, Urban, Cave, Maze, Mine, Shipyard, Ruins, Jungle)?
- What Isaac Replicator randomization presets should be prioritized for Phase 1?
- Should we implement custom USD scene generation scripts or leverage Isaac Lab's scene composition tools?
- Which kinodynamic planner parameters (velocity/acceleration bounds) should be the default for early tests?
- Do we need additional logging topics (e.g., actuator commands) beyond the Phase 2 minimum (`/depth`, `/odom`, `/imu`) for later QC?

## Upcoming Actions
- Install ROS 2 Humble for Windows and verify Isaac Sim ROS 2 bridge compatibility.
- Create environment configuration manifests in `config/env/`:
  - `isaac_lab_env.yaml` — Environment specifications
  - `setup_instructions.md` — Complete setup documentation
  - `sensors.yaml` — Stereo depth, IMU, odometry configurations
  - `scenes_config.yaml` — Scene family definitions and randomization parameters
- Create ROS 2 bridge configuration in `config/ros2/`:
  - `bridge_topics.yaml` — Topic specifications with message types and QoS
- Implement Isaac Lab environment wrapper in `src/sim/environment.py`
- Create scene generation and validation scripts in `scripts/`
- Populate `.\data\raw\runtime\` directory structure for logging
- Complete Phase 1 checklist items documented in `docs/phase1_checklist.md`

## Phase 1 Progress Tracking
**Started:** 2025-10-27
**Target Completion:** TBD (based on ROS 2 installation complexity)

**Completed:**
- Updated `docs/plan.md` Phase 1 section for Isaac Lab approach
- Updated `README.md` with Phase 1 active status and environment setup documentation
- Documented platform decisions and assumptions in owner log

**In Progress:**
- Creating configuration files for environment and ROS 2 setup
- Updating TODO files across modules

**Blocked:**
- ROS 2 Humble installation (prerequisite for bridge testing)

## Historical Decisions
- **2025-10-28:** Prioritize Phase 2 planner scaffolding before completing Phase 1 Isaac Sim setup to unblock code structure and logging specs. *(REVERSED on 2025-10-27 - now prioritizing Phase 1)*
- **2025-10-28:** Recreate architecture diagrams later; focus on textual documentation (`docs/plan.md`, `RAPID.pdf`) for immediate planning.
