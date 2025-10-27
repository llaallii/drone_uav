# RAPID v2 Drone Autonomy Sandbox

RAPID v2 is a single-operator effort to build an end-to-end autonomous drone pipeline: Isaac Sim environment setup, expert trajectory generation, dataset curation, inverse reinforcement learning, and sim-to-real deployment. The detailed eleven-phase roadmap lives in `docs/plan.md`.

## Roadmap Snapshot
- **Phase 1:** Isaac Sim foundation, reproducible scenes, ROS 2 bridge.
- **Phase 2:** Expert planner stack (mapping, kinodynamic global planner, 10 Hz replanner).
- **Phase 3-5:** Controller integration, logging, QC scorecards.
- **Phase 6-8:** Curriculum expansion, dataset freeze, release packaging.
- **Phase 9-11:** IRL training, sim-to-real fine-tuning, continuous learning loop.

Refer to `docs/plan.md` for full objectives, deliverables, and success criteria.

## Repository Layout
- `docs/` &mdash; Planning artifacts, owner notes, and future design diagrams.
- `src/` &mdash; Python modules for simulation, planning, control, and analysis.
- `config/` &mdash; Environment and ROS 2 manifests, planner parameters.
- `data/` &mdash; Raw logs, processed shards, QC reports, schema definitions.
- `tools/`, `scripts/` &mdash; Utility code and runnable automation entry points.
- `tests/` &mdash; Placeholder unit and integration tests to grow with implementation.
- `infra/`, `experiments/` &mdash; CI scaffolding and experiment tracking space.

Each directory contains a `notes.md` describing its role in the pipeline and a `todo.md` with outstanding tasks.

## Current Status
- directories currently contain placeholders awaiting implementation.
- `RAPID.pdf` and `docs/plan.md` restored; architecture diagrams still need to be recreated.
- Phase 1 setup is deferred while groundwork for Phase 2 planner integration is prepared.

## Next Steps
1. Keep `docs/owner_log.md` current with decisions, assumptions, and blockers.
2. Define planner data structures, configuration schemas, and logging contracts.
3. Replace module TODO stubs with incremental functionality and accompanying tests.
