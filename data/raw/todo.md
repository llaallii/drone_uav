# TODO - Raw Data Management

## Phase 1 - Runtime Logging Setup

### Directory Structure
- [ ] Create `.\data\raw\runtime\` for live logging
- [ ] Create `.\data\raw\runtime\sensors\` for sensor data
  - [ ] `.\data\raw\runtime\sensors\depth\`
  - [ ] `.\data\raw\runtime\sensors\imu\`
  - [ ] `.\data\raw\runtime\sensors\odom\`
- [ ] Create `.\data\raw\scenes\` for scene storage
  - [ ] `.\data\raw\scenes\cache\` for USD scene files
- [ ] Set up scene seed log: `.\data\raw\runtime\scenes.jsonl`

### Logging Implementation
- [ ] Implement sensor data logging in `src/sim/data_logger.py`
  - [ ] Depth camera logging (LZ4 compressed images)
  - [ ] IMU logging (downsampled from 100Hz to 20Hz)
  - [ ] Odometry logging (20Hz)
  - [ ] Include timestamps in all logs
  - [ ] Include sensor configuration metadata
  - [ ] Include simulation parameters (dt, frame rate)
- [ ] Implement buffered writing (100MB buffer, 5s flush interval)
- [ ] Add log rotation/cleanup for runtime logs

### Scene Seed Logging
- [ ] Define `scenes.jsonl` format
  ```json
  {
    "seed": 12345,
    "family": "office",
    "timestamp": "2025-10-27T...",
    "config": {...},
    "usd_path": ".\data\raw\scenes\cache\office_12345.usd"
  }
  ```
- [ ] Implement scene seed logging in scene generator
- [ ] Add scene metadata (dimensions, asset counts, etc.)
- [ ] Support scene seed lookup for reproducibility

### Storage Management
- [ ] Define storage limits for runtime logs
  - [ ] Disk space monitoring
  - [ ] Auto-cleanup of old runtime logs
  - [ ] Preserve scene seeds indefinitely
- [ ] Implement pruning strategy
  - [ ] Keep last N days of runtime logs
  - [ ] Archive important episodes before pruning
  - [ ] Never delete scene seeds (needed for reproduction)

### Data Ingestion (Phase 4+)
- [ ] Define ingestion procedure from runtime logs
  - [ ] Raw logs → processed episodes
  - [ ] Episode validation (completeness, QC)
  - [ ] Shard packing (100-200 episodes per shard)
- [ ] Implement shard creation pipeline
- [ ] Create global index (Parquet format)

## Phase 4 - Episode Logging
- [ ] Define episode data format
  - [ ] Depth sequences (K=4 frames)
  - [ ] Odometry, velocities, quaternions
  - [ ] Actions (Δr, Δψ)
  - [ ] QC flags (feasibility, tracking error, sensor validity)
- [ ] Implement episode recording in `src/sim/data_logger.py`
- [ ] Log episodes to `.\data\raw\episodes\`

## Phase 5 - Quality Control Integration
- [ ] Add QC metadata to episode logs
- [ ] Flag invalid data points (sensor failures, tracking errors)
- [ ] Generate per-episode QC scores

## Notes
- Runtime logs are temporary (pruned regularly)
- Scene seeds are permanent (needed for dataset reproduction)
- Episodes (Phase 4+) are the primary dataset artifacts
- Use LZ4 compression for depth images (fast compression/decompression)
- JSONL format for scene seeds (append-only, easy parsing)
- Windows paths use backslash notation
