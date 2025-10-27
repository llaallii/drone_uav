# RAPID v2 Environment Setup Instructions

Complete setup guide for Phase 1 environment configuration on Ubuntu 24.04 LTS.

## Prerequisites

### System Requirements
- **Operating System:** Ubuntu 24.04 LTS (64-bit)
- **GPU:** NVIDIA RTX/Tesla series (CUDA 12.8 compatible)
- **VRAM:** Minimum 8GB (16GB recommended)
- **RAM:** Minimum 16GB (32GB recommended)
- **Disk Space:** 50GB+ free space

### Software Requirements
- **Miniconda/Anaconda:** Python environment management
- **Git:** Version control
- **NVIDIA Drivers:** Latest stable drivers for CUDA 12.8

---

## 1. Isaac Sim 5.0.0 Installation ✅ COMPLETED

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

The environment was created with the following steps:

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

## 2. ROS 2 Jazzy Installation ✅ COMPLETED

ROS 2 Jazzy is required for the Isaac Sim ROS 2 bridge and Phase 2 planner integration.

### Installation Verification

Your system already has ROS 2 Jazzy installed. To verify:

```bash
# Check ROS 2 installation
ros2 --version

# Expected output: ros2 cli version: jazzy
echo $ROS_DISTRO

# Expected output: jazzy
```

### Installation Reference (For Documentation)

ROS 2 Jazzy was installed on Ubuntu 24.04 using the following steps:

1. **Set up ROS 2 apt repository:**
   ```bash
   sudo apt update && sudo apt install -y software-properties-common
   sudo add-apt-repository universe
   sudo apt update && sudo apt install curl -y
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

2. **Install ROS 2 Jazzy:**
   ```bash
   sudo apt update
   sudo apt install -y ros-jazzy-desktop
   ```

3. **Install development tools:**
   ```bash
   sudo apt install -y python3-colcon-common-extensions python3-rosdep
   ```

4. **Set up ROS 2 environment:**
   ```bash
   echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
   source ~/.bashrc
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

## 3. Isaac Lab Setup ✅ COMPLETED

Isaac Lab provides robotics utilities, sensors, and RL tools built on top of Isaac Sim.

### Installation Verification

To verify Isaac Lab is installed in your environment:

```bash
# Activate environment
conda activate env_isaaclab

# Check if Isaac Lab is accessible
python -c "import omni.isaac.lab; print('Isaac Lab installed successfully')"
```

### Installation Reference (For Documentation)

Isaac Lab was installed using the following steps:

```bash
# Activate environment
conda activate env_isaaclab

# Clone Isaac Lab repository
cd /home/lali/Desktop
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Run installation script
./isaaclab.sh --install

# Verify installation
./isaaclab.sh -p source/standalone/tutorials/00_sim/create_empty.py
```

Isaac Lab provides:
1. Advanced sensor APIs (cameras, IMU, depth sensors)
2. Robot articulation and control utilities
3. ROS 2 bridge integration
4. RL environment templates
5. Scene composition and randomization tools

---

## 4. Project Environment Configuration

### Directory Structure Setup

Create required directories for Phase 1:

```bash
# From project root (/home/lali/Desktop/drone_uav)
mkdir -p data/raw/runtime
mkdir -p data/raw/runtime/sensors
mkdir -p data/raw/scenes
mkdir -p data/dataset/shards
```

Or use the setup script to create all required directories:

```bash
python scripts/setup_sim.py --fix-dirs
```

### Environment Activation Workflow

Create a convenience script `activate_env.sh`:

```bash
#!/bin/bash
echo "Activating RAPID v2 environment..."

# Activate conda environment
source ~/miniconda3/bin/activate env_isaaclab

# Load ROS 2 Jazzy
if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
    echo "ROS 2 Jazzy loaded"
else
    echo "WARNING: ROS 2 not found. Install for full Phase 1 functionality."
fi

# Set project root
export RAPID_ROOT=$(pwd)
echo "RAPID_ROOT=$RAPID_ROOT"

# Verify setup
echo ""
echo "Verifying installation..."
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
pip show isaacsim | grep Version

echo ""
echo "Environment ready. Use 'isaacsim' to launch Isaac Sim."
```

Make the script executable and use it:
```bash
cd /home/lali/Desktop/drone_uav
chmod +x activate_env.sh
source activate_env.sh
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
# Check ROS 2 version
ros2 --version

# Check ROS distribution
echo $ROS_DISTRO

# List ROS 2 topics (should be empty initially)
ros2 topic list
```

### Project Structure Verification

```bash
# Verify directories exist
ls -la data/raw/runtime
ls -la config/env
ls -la config/ros2

# Verify config files
cat config/env/isaac_lab_env.yaml
cat config/env/sensors.yaml
cat config/env/scenes_config.yaml
cat config/ros2/bridge_topics.yaml
```

### Integration Test

```bash
# Run Phase 1 setup verification script
conda activate env_isaaclab
python scripts/setup_sim.py

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

1. **Implement Isaac Sim environment wrapper:**
   ```bash
   # Edit src/sim/environment.py to implement sensor and scene loading
   ```

2. **Create scene generation scripts:**
   ```bash
   # Implement scripts/generate_scenes.py for procedural scene generation
   ```

3. **Test ROS 2 bridge integration:**
   ```bash
   # Create and test scripts/test_ros2_bridge.py
   ```

4. **Generate test scenes:**
   ```bash
   python scripts/generate_scenes.py --family office --count 5
   ```

5. **Review Phase 1 checklist:**
   - See [docs/phase1_checklist.md](docs/phase1_checklist.md) for completion criteria

---

## Reference

- **Isaac Sim Docs:** https://docs.omniverse.nvidia.com/isaacsim/latest/
- **Isaac Lab Docs:** https://isaac-sim.github.io/IsaacLab/
- **ROS 2 Jazzy Docs:** https://docs.ros.org/en/jazzy/
- **Project Plan:** [docs/plan.md](docs/plan.md)
- **Owner Log:** [docs/owner_log.md](docs/owner_log.md)
