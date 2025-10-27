# RAPID v2 Environment Setup Instructions

Complete setup guide for Phase 1 environment configuration on Windows.

## Prerequisites

### System Requirements
- **Operating System:** Windows 10/11 (64-bit)
- **GPU:** NVIDIA RTX/Tesla series (CUDA 12.8 compatible)
- **VRAM:** Minimum 8GB (16GB recommended)
- **RAM:** Minimum 16GB (32GB recommended)
- **Disk Space:** 50GB+ free space

### Software Requirements
- **Miniconda/Anaconda:** Python environment management
- **Git:** Version control
- **NVIDIA Drivers:** Latest stable drivers for CUDA 12.8

---

## 1. Isaac Sim 5.0.0 Installation (Already Completed)

Your existing `env_isaaclab` environment already has Isaac Sim 5.0.0 installed. To verify:

```bash
# Activate environment
conda activate env_isaaclab

# Verify Isaac Sim installation
pip show isaacsim

# Expected output:
# Name: isaacsim
# Version: 5.0.0.0
```

### Isaac Sim Installation Reference (For Documentation)

If you need to recreate the environment, here are the steps that were followed:

```bash
# Create conda environment with Python 3.11
conda create -n env_isaaclab python=3.11
conda activate env_isaaclab

# Install PyTorch with CUDA 12.8 support
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128

# Install Isaac Sim 5.0.0
pip install "isaacsim[all,extscache]==5.0.0" --extra-index-url https://pypi.nvidia.com
```

### First Launch

When running Isaac Sim for the first time:

```bash
conda activate env_isaaclab
isaacsim
```

**Note:** First launch may take 10-15 minutes to pull dependent extensions from the registry.

---

## 2. ROS 2 Humble Installation (Required)

ROS 2 Humble is required for the Isaac Sim ROS 2 bridge and Phase 2 planner integration.

### Installation Steps

1. **Download ROS 2 Humble for Windows:**
   - Visit: https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html
   - Download the latest Humble binary release

2. **Install ROS 2 Humble:**
   - Extract the archive to `C:\dev\ros2_humble`
   - Or your preferred location (update paths accordingly)

3. **Set up environment variables:**

   Create a batch file `setup_ros2.bat`:

   ```batch
   @echo off
   call C:\dev\ros2_humble\local_setup.bat
   echo ROS 2 Humble environment loaded
   ```

4. **Verify ROS 2 installation:**

   ```bash
   # Open new Command Prompt
   call setup_ros2.bat
   ros2 --version

   # Expected output: ros2 cli version: humble
   ```

5. **Install additional ROS 2 packages:**

   ```bash
   # With ROS 2 environment loaded
   pip install colcon-common-extensions
   ```

### Isaac Sim ROS 2 Bridge Setup

The Isaac Sim ROS 2 bridge connects simulation topics to ROS 2:

1. **Verify bridge availability:**

   ```bash
   conda activate env_isaaclab
   python -c "from isaacsim import SimulationApp; print('Bridge available')"
   ```

2. **Bridge configuration:**
   - Topic specifications: `config/ros2/bridge_topics.yaml`
   - Launch configuration: TBD in Phase 1 implementation

---

## 3. Isaac Lab Setup (Optional but Recommended)

Isaac Lab provides robotics utilities, sensors, and RL tools.

### Installation

```bash
# Activate environment
conda activate env_isaaclab

# Clone Isaac Lab repository
cd C:\Users\ratan\Desktop
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Run installation script (for Linux, adapt for Windows)
# Note: isaaclab.sh is a bash script - may need WSL or manual installation on Windows
# For now, we'll use Isaac Sim's built-in capabilities
```

**Windows Note:** Isaac Lab's installation script is designed for Linux. On Windows, we'll:
1. Use Isaac Sim's built-in sensor/robot APIs directly
2. Leverage Isaac Sim Python API for scene management
3. Implement custom wrappers in `src/sim/environment.py`

---

## 4. Project Environment Configuration

### Directory Structure Setup

Create required directories for Phase 1:

```bash
# From project root (C:\Users\ratan\Desktop\drone_uav)
mkdir data\raw\runtime
mkdir data\raw\runtime\sensors
mkdir data\raw\scenes
mkdir data\dataset\shards
```

### Environment Activation Workflow

Create a convenience script `activate_env.bat`:

```batch
@echo off
echo Activating RAPID v2 environment...

REM Activate conda environment
call conda activate env_isaaclab

REM Load ROS 2 (if installed)
if exist C:\dev\ros2_humble\local_setup.bat (
    call C:\dev\ros2_humble\local_setup.bat
    echo ROS 2 Humble loaded
) else (
    echo WARNING: ROS 2 not found. Install for full Phase 1 functionality.
)

REM Set project root
set RAPID_ROOT=%CD%
echo RAPID_ROOT=%RAPID_ROOT%

REM Verify setup
echo.
echo Verifying installation...
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
pip show isaacsim | findstr Version

echo.
echo Environment ready. Use 'isaacsim' to launch Isaac Sim.
```

Usage:
```bash
cd C:\Users\ratan\Desktop\drone_uav
activate_env.bat
```

---

## 5. Verification Checklist

Run these commands to verify your Phase 1 setup:

### Isaac Sim Verification

```bash
conda activate env_isaaclab

# Check Isaac Sim version
pip show isaacsim

# Launch Isaac Sim (headless check)
isaacsim --help

# Verify CUDA/PyTorch
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda)"
```

### ROS 2 Verification

```bash
# Load ROS 2 environment
call setup_ros2.bat

# Check ROS 2 version
ros2 --version

# List ROS 2 topics (should be empty initially)
ros2 topic list
```

### Project Structure Verification

```bash
# Verify directories exist
dir data\raw\runtime
dir config\env
dir config\ros2

# Verify config files
type config\env\isaac_lab_env.yaml
type config\env\sensors.yaml
type config\env\scenes_config.yaml
type config\ros2\bridge_topics.yaml
```

### Integration Test

```bash
# Run Phase 1 setup verification script
conda activate env_isaaclab
python scripts\setup_sim.py

# Expected output: Environment checks passed
```

---

## 6. Troubleshooting

### Isaac Sim won't launch

**Issue:** `isaacsim` command not found

**Solution:**
```bash
# Verify environment is activated
conda activate env_isaaclab

# Reinstall if needed
pip install --force-reinstall "isaacsim[all,extscache]==5.0.0" --extra-index-url https://pypi.nvidia.com
```

### CUDA not available

**Issue:** `torch.cuda.is_available()` returns `False`

**Solution:**
1. Update NVIDIA drivers to latest version
2. Verify CUDA 12.8 compatible GPU
3. Reinstall PyTorch with correct CUDA version:
   ```bash
   pip install --force-reinstall torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
   ```

### ROS 2 bridge connection issues

**Issue:** Topics not appearing in `ros2 topic list`

**Solution:**
1. Verify ROS 2 environment is loaded in same terminal as Isaac Sim
2. Check bridge configuration in `config/ros2/bridge_topics.yaml`
3. Restart Isaac Sim with bridge enabled (see Phase 1 scripts)

### First launch takes forever

**Issue:** Isaac Sim hangs on first launch

**Expected Behavior:** First launch downloads extension cache (10-15 minutes)

**Solution:**
- Be patient on first launch
- Ensure stable internet connection
- Subsequent launches will be much faster

---

## 7. Next Steps

After completing environment setup:

1. **Test sensor configuration:**
   ```bash
   python scripts/test_sensors.py
   ```

2. **Generate test scenes:**
   ```bash
   python scripts/generate_scenes.py --family office --count 5
   ```

3. **Verify ROS 2 bridge:**
   ```bash
   python scripts/test_ros2_bridge.py
   ```

4. **Review Phase 1 checklist:**
   - See `docs/phase1_checklist.md` for completion criteria

---

## Reference

- **Isaac Sim Docs:** https://docs.omniverse.nvidia.com/isaacsim/latest/
- **Isaac Lab Docs:** https://isaac-sim.github.io/IsaacLab/
- **ROS 2 Humble Docs:** https://docs.ros.org/en/humble/
- **Project Plan:** `docs/plan.md`
- **Owner Log:** `docs/owner_log.md`
