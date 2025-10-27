# Owner Log

Central thread for decisions, assumptions, and follow-ups while executing the RAPID v2 roadmap as a solo project.

## Active Decisions
- 2025-10-28: Prioritize Phase 2 planner scaffolding before completing Phase 1 Isaac Sim setup to unblock code structure and logging specs.
- 2025-10-28: Recreate architecture diagrams later; focus on textual documentation (`docs/plan.md`, `RAPID.pdf`) for immediate planning.

## Assumptions
- Isaac Sim 2023.1+ remains the baseline; no newer breaking changes expected before Phase 1 resumes.
- ROS 2 topic interfaces `/depth`, `/odom`, `/imu` will be sufficient for planner MVP as outlined in `docs/plan.md`.
- Single-operator workflow means automation (scripts/tests) must offset lack of parallel work.

## Open Questions
- What scene randomization presets are required from RAPID.pdf once diagrams return?
- Which kinodynamic planner parameters (velocity/acceleration bounds) should be the default for early tests?
- Do we need additional logging topics (e.g., actuator commands) beyond the Phase 2 minimum for later QC?

## Upcoming Actions
- Draft detailed planner interface notes in `docs/interfaces/planning.md`.
- Populate `config/env/` and `config/ros2/` with initial manifests.
- Begin translating TODO stubs in `src/planning/` into functional modules with tests.
