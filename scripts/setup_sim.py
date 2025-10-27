"""Script to verify Phase 1 environment setup for RAPID v2.

This script checks all prerequisites for Phase 1:
- Isaac Sim 5.0.0 installation
- Python 3.11 and dependencies
- CUDA availability
- ROS 2 Humble installation
- Directory structure
- Configuration files
- Basic Isaac Sim functionality

Usage:
    python scripts/setup_sim.py
    python scripts/setup_sim.py --verbose
    python scripts/setup_sim.py --fix-dirs  # Create missing directories
"""

import sys
import subprocess
from pathlib import Path
import argparse


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_python_version():
    """Check Python version is 3.11."""
    print_header("Checking Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor == 11:
        print_success(f"Python version: {version_str}")
        return True
    else:
        print_error(f"Python version: {version_str} (Expected 3.11.x)")
        print("  Fix: Activate env_isaaclab conda environment")
        print("       conda activate env_isaaclab")
        return False


def check_isaac_sim():
    """Check Isaac Sim installation."""
    print_header("Checking Isaac Sim Installation")

    try:
        result = subprocess.run(
            ["pip", "show", "isaacsim"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Parse version from output
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    version = line.split(':')[1].strip()
                    if version.startswith('5.0.0'):
                        print_success(f"Isaac Sim installed: {version}")
                        return True
                    else:
                        print_warning(f"Isaac Sim version {version} (Expected 5.0.0.x)")
                        return True  # Allow other 5.x versions

            print_error("Isaac Sim installed but version not found")
            return False
        else:
            print_error("Isaac Sim not installed")
            print("  Fix: Install Isaac Sim 5.0.0")
            print("       pip install \"isaacsim[all,extscache]==5.0.0\" --extra-index-url https://pypi.nvidia.com")
            return False

    except Exception as e:
        print_error(f"Error checking Isaac Sim: {e}")
        return False


def check_cuda():
    """Check CUDA availability via PyTorch."""
    print_header("Checking CUDA Availability")

    try:
        import torch
        cuda_available = torch.cuda.is_available()

        if cuda_available:
            cuda_version = torch.version.cuda
            device_name = torch.cuda.get_device_name(0)
            print_success(f"CUDA available: {cuda_version}")
            print_success(f"GPU: {device_name}")
            return True
        else:
            print_error("CUDA not available")
            print("  Fix: Install NVIDIA drivers and CUDA 12.8")
            print("       Reinstall PyTorch: pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128")
            return False

    except ImportError:
        print_error("PyTorch not installed")
        print("  Fix: Install PyTorch with CUDA support")
        print("       pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128")
        return False


def check_ros2():
    """Check ROS 2 installation."""
    print_header("Checking ROS 2 Installation")

    try:
        result = subprocess.run(
            ["ros2", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            version = result.stdout.strip()
            if "jazzy" in version.lower():
                print_success(f"ROS 2 installed: {version}")
                return True
            elif "humble" in version.lower():
                print_warning(f"ROS 2 Humble found (expected Jazzy): {version}")
                print("  Consider upgrading to ROS 2 Jazzy for Ubuntu 24.04")
                return True  # Allow Humble but recommend Jazzy
            else:
                print_warning(f"ROS 2 installed: {version} (expected Jazzy)")
                print("  Expected: ROS 2 Jazzy for Ubuntu 24.04")
                return True  # Allow other distributions

        else:
            print_error("ROS 2 not found")
            print("  Fix: Install ROS 2 Jazzy for Ubuntu 24.04")
            print("       See: config/env/setup_instructions.md")
            return False

    except FileNotFoundError:
        print_error("ROS 2 not found in PATH")
        print("  Fix: Install ROS 2 Jazzy and source the setup file")
        print("       source /opt/ros/jazzy/setup.bash")
        print("       Or add to ~/.bashrc for automatic loading")
        return False
    except Exception as e:
        print_error(f"Error checking ROS 2: {e}")
        return False


def check_directory_structure(fix=False):
    """Check required directory structure exists."""
    print_header("Checking Directory Structure")

    required_dirs = [
        Path("data/raw/runtime"),
        Path("data/raw/runtime/sensors"),
        Path("data/raw/runtime/sensors/depth"),
        Path("data/raw/runtime/sensors/imu"),
        Path("data/raw/runtime/sensors/odom"),
        Path("data/raw/scenes"),
        Path("data/raw/scenes/cache"),
        Path("data/dataset/shards"),
    ]

    all_exist = True

    for dir_path in required_dirs:
        if dir_path.exists():
            print_success(f"Directory exists: {dir_path}")
        else:
            if fix:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"Created directory: {dir_path}")
            else:
                print_error(f"Directory missing: {dir_path}")
                all_exist = False

    if not all_exist and not fix:
        print("\n  Fix: Run with --fix-dirs to create missing directories")
        print("       python scripts/setup_sim.py --fix-dirs")

    return all_exist or fix


def check_config_files():
    """Check required configuration files exist."""
    print_header("Checking Configuration Files")

    required_configs = [
        Path("config/env/isaac_lab_env.yaml"),
        Path("config/env/sensors.yaml"),
        Path("config/env/scenes_config.yaml"),
        Path("config/ros2/bridge_topics.yaml"),
    ]

    all_exist = True

    for config_path in required_configs:
        if config_path.exists():
            print_success(f"Config exists: {config_path}")
        else:
            print_error(f"Config missing: {config_path}")
            all_exist = False

    if not all_exist:
        print("\n  Fix: Ensure all configuration files are committed to version control")

    return all_exist


def check_isaac_sim_launch():
    """Check Isaac Sim can be launched (basic test)."""
    print_header("Checking Isaac Sim Launch")

    try:
        result = subprocess.run(
            ["isaacsim", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print_success("Isaac Sim launch command works")
            return True
        else:
            print_error("Isaac Sim launch command failed")
            print(f"  Error: {result.stderr}")
            return False

    except FileNotFoundError:
        print_error("'isaacsim' command not found")
        print("  Fix: Activate env_isaaclab conda environment")
        return False
    except subprocess.TimeoutExpired:
        print_warning("Isaac Sim launch check timed out (may be downloading extensions)")
        return True  # Allow timeout on first run
    except Exception as e:
        print_error(f"Error launching Isaac Sim: {e}")
        return False


def main():
    """Run all verification checks."""
    parser = argparse.ArgumentParser(description="Verify RAPID v2 Phase 1 environment setup")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--fix-dirs", action="store_true", help="Create missing directories")
    args = parser.parse_args()

    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}RAPID v2 - Phase 1 Environment Verification{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Isaac Sim Installation", check_isaac_sim),
        ("CUDA Availability", check_cuda),
        ("ROS 2 Installation", check_ros2),
        ("Directory Structure", lambda: check_directory_structure(fix=args.fix_dirs)),
        ("Configuration Files", check_config_files),
        ("Isaac Sim Launch", check_isaac_sim_launch),
    ]

    results = {}
    for name, check_func in checks:
        results[name] = check_func()

    # Summary
    print_header("Verification Summary")

    passed = sum(results.values())
    total = len(results)

    for name, result in results.items():
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")

    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.END}\n")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Environment setup complete! Ready for Phase 1 implementation.{Colors.END}\n")
        print("Next steps:")
        print("  1. Implement Isaac Sim environment wrapper (src/sim/environment.py)")
        print("  2. Create scene generation scripts (scripts/generate_scenes.py)")
        print("  3. Test ROS 2 Jazzy bridge (scripts/test_ros2_bridge.py)")
        print("  4. Generate and validate test scenes (10-20 across families)")
        print("  5. Review Phase 1 checklist (docs/phase1_checklist.md)")
        print("\n Platform: Ubuntu 24.04 LTS | ROS 2: Jazzy | Isaac Sim: 5.0.0")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Environment setup incomplete. Fix errors above.{Colors.END}\n")
        print("See config/env/setup_instructions.md for detailed setup guide.")
        print("Platform: Ubuntu 24.04 LTS | Expected ROS 2: Jazzy")
        return 1


if __name__ == '__main__':
    sys.exit(main())
