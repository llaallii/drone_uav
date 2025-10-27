# Owner Log

Central thread for decisions, assumptions, and follow-ups while executing the RAPID v2 roadmap as a solo project.

## Active Decisions
- **2025-10-27:** **PLATFORM MIGRATION:** Migrated development environment from Windows to Ubuntu 24.04 LTS for better ROS 2 and Isaac Sim compatibility.
- **2025-10-27:** **ROS 2 UPGRADE:** Upgraded from ROS 2 Humble to ROS 2 Jazzy to match Ubuntu 24.04 LTS native support.
- **2025-10-27:** Phase 1 is now ACTIVE. Pivoting from deferred Phase 1 to immediate environment setup.
- **2025-10-27:** Using Isaac Lab framework (hybrid approach) instead of raw Isaac Sim for better sensor/ROS 2 integration and RL-ready infrastructure.
- **2025-10-27:** Adopting pip-based Isaac Sim 5.0.0 installation in `env_isaaclab` conda environment instead of binary installation at `/opt/NVIDIA/isaac_sim`.
- **2025-10-27:** Using monorepo structure at current project root instead of multi-repo workspace (`~/rapid_v2_ws` with separate repos).
- **2025-10-27:** Using Linux paths (`./data/`, `/opt/ros/jazzy/`) for Ubuntu 24.04 environment.
- **2025-10-27:** Leveraging both Isaac Lab assets and custom procedural scene generation for 10 scene families.

## Assumptions
- Isaac Sim 5.0.0 remains stable; no breaking changes expected before Phase 1 completion.
- ROS 2 Jazzy on Ubuntu 24.04 provides better compatibility and performance than Humble on Windows.
- Isaac Lab's sensor framework (cameras, IMU, odometry) will meet Phase 1-2 requirements.
- Ubuntu 24.04 LTS environment provides superior support for simulation + ROS 2 + planning pipeline compared to Windows.
- Single-operator workflow means automation (scripts/tests) must offset lack of parallel work.
- Isaac Lab's abstractions won't conflict with Fast-Planner integration in Phase 2.
- Linux paths (`./data/`) provide better compatibility with ROS 2 and Isaac Lab ecosystem.
- Migration to Linux will improve long-term maintainability and deployment options.

## Platform & Setup Notes
- **Operating System:** Ubuntu 24.04 LTS (Noble Numbat) - **MIGRATED from Windows**
- **Isaac Sim Version:** 5.0.0 (installed via pip, not binary)
- **Python Version:** 3.11 (in `env_isaaclab` conda environment)
- **PyTorch Version:** 2.7.0 with CUDA 12.8 support
- **Isaac Lab:** Installed and integrated - provides sensors, robots, ROS 2 bridge, RL utilities
- **ROS 2 Distribution:** Jazzy (native to Ubuntu 24.04) - **UPGRADED from Humble**
- **Workspace Structure:** Monorepo at `/home/lali/Desktop/drone_uav` (changed from Windows path)
- **CUDA/GPU:** NVIDIA GPU with CUDA 12.8 support confirmed functional

## Open Questions
- What are the specific performance characteristics of Isaac Lab vs raw Isaac Sim for our drone simulation needs?
- ~~Will ROS 2 Humble on Windows have any latency/performance issues compared to Linux?~~ **RESOLVED:** Migrated to Ubuntu 24.04 with ROS 2 Jazzy for optimal performance.
- Which Isaac Lab assets are suitable for our 10 scene families (Office, Warehouse, Forest, Urban, Cave, Maze, Mine, Shipyard, Ruins, Jungle)?
- What Isaac Replicator randomization presets should be prioritized for Phase 1?
- Should we implement custom USD scene generation scripts or leverage Isaac Lab's scene composition tools?
- Which kinodynamic planner parameters (velocity/acceleration bounds) should be the default for early tests?
- Do we need additional logging topics (e.g., actuator commands) beyond the Phase 2 minimum (`/depth`, `/odom`, `/imu`) for later QC?
- How does ROS 2 Jazzy's new features compare to Humble for our use case?

## Upcoming Actions
- ~~Install ROS 2 Humble for Windows and verify Isaac Sim ROS 2 bridge compatibility.~~ **COMPLETED:** ROS 2 Jazzy installed on Ubuntu 24.04
- ~~Create environment configuration manifests in `config/env/`:~~ **COMPLETED:**
  - ~~`isaac_lab_env.yaml` — Environment specifications~~
  - ~~`setup_instructions.md` — Complete setup documentation~~
  - ~~`sensors.yaml` — Stereo depth, IMU, odometry configurations~~
  - ~~`scenes_config.yaml` — Scene family definitions and randomization parameters~~
- ~~Create ROS 2 bridge configuration in `config/ros2/`:~~ **COMPLETED:**
  - ~~`bridge_topics.yaml` — Topic specifications with message types and QoS~~
- **IN PROGRESS:** Implement Isaac Lab environment wrapper in `src/sim/environment.py`
- **NEXT:** Create scene generation and validation scripts in `scripts/`
  - `scripts/generate_scenes.py` — Individual scene generation
  - `scripts/batch_generate_scenes.py` — Batch generation for all families
  - `scripts/visualize_scene.py` — Scene inspection utility
- **NEXT:** Test and validate ROS 2 Jazzy bridge with Isaac Sim
- **NEXT:** Populate `./data/raw/runtime/` directory structure for logging
- **ONGOING:** Complete Phase 1 checklist items documented in `docs/phase1_checklist.md`

## Phase 1 Progress Tracking
**Started:** 2025-10-27
**Platform Migration:** 2025-10-27 (Windows → Ubuntu 24.04)
**Target Completion:** TBD (environment setup completed, implementation in progress)

**Completed:** ✅
- **Platform Migration:** Successfully migrated from Windows to Ubuntu 24.04 LTS
- **Environment Setup:** Isaac Sim 5.0.0, Python 3.11, PyTorch 2.7.0, CUDA 12.8
- **ROS 2 Installation:** ROS 2 Jazzy installed and verified
- **Isaac Lab:** Installed and integrated into conda environment
- **Configuration Files:** All YAML configs created (env, sensors, scenes, ROS 2 bridge)
- **Documentation:** Updated all docs for Ubuntu 24.04 and ROS 2 Jazzy
  - Updated `docs/plan.md` Phase 1 section for Isaac Lab approach
  - Updated `README.md` with Phase 1 active status and environment setup
  - Updated `config/env/setup_instructions.md` for Ubuntu 24.04
  - Updated `docs/phase1_checklist.md` with completed items
  - Updated `docs/owner_log.md` with platform migration notes
- **Verification Script:** `scripts/setup_sim.py` updated for new platform

**In Progress:**
- Isaac Lab environment wrapper implementation (`src/sim/environment.py`)
- Scene generation scripts development
- ROS 2 bridge integration and testing

**No Blockers:** ✅ All prerequisites installed and verified

## Historical Decisions
- **2025-10-28:** Prioritize Phase 2 planner scaffolding before completing Phase 1 Isaac Sim setup to unblock code structure and logging specs. *(REVERSED on 2025-10-27 - now prioritizing Phase 1)*
- **2025-10-28:** Recreate architecture diagrams later; focus on textual documentation (`docs/plan.md`, `RAPID.pdf`) for immediate planning.
