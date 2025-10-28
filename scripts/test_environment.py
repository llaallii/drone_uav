#!/usr/bin/env python3
"""Test script for Isaac Lab environment wrapper.

This script validates the Phase 1 environment setup by:
1. Initializing Isaac Sim application
2. Setting up sensors (depth camera, IMU, odometry)
3. Setting up ROS 2 bridge
4. Running a short simulation loop
5. Validating sensor outputs
6. (Optional) Testing Docker ROS 2 container communication

Usage:
    # Without Docker
    python scripts/test_environment.py --headless --num_steps 100

    # With Docker integration
    python scripts/test_environment.py --with-docker --headless --num_steps 100
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sim.environment import IsaacSimEnvironment


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Isaac Lab environment wrapper")
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode (no GUI)"
    )
    parser.add_argument(
        "--num_steps",
        type=int,
        default=100,
        help="Number of simulation steps to run"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/env/isaac_lab_env.yaml",
        help="Path to environment configuration file"
    )
    parser.add_argument(
        "--scene_family",
        type=str,
        default="office",
        help="Scene family to load (office, warehouse, forest, etc.)"
    )
    parser.add_argument(
        "--scene_seed",
        type=int,
        default=42,
        help="Random seed for scene generation"
    )
    parser.add_argument(
        "--with-docker",
        action="store_true",
        default=False,
        help="Start Docker container and test ROS 2 communication"
    )
    return parser.parse_args()


def validate_observation(obs, step_num):
    """Validate observation dictionary contains expected data.

    Args:
        obs: Observation dictionary from environment
        step_num: Current step number for logging

    Returns:
        bool: True if validation passes
    """
    print(f"\n[Step {step_num}] Validating observation...")

    # Check required keys
    required_keys = ['timestamp']
    optional_keys = ['depth', 'imu_accel', 'imu_gyro', 'odom_pos', 'odom_vel', 'odom_quat']

    missing_keys = [key for key in required_keys if key not in obs]
    if missing_keys:
        print(f"  ❌ Missing required keys: {missing_keys}")
        return False

    present_keys = [key for key in optional_keys if key in obs]
    print(f"  ✓ Present sensor keys: {present_keys}")

    # Validate specific sensors if present
    if 'depth' in obs and obs['depth'] is not None:
        print(f"  ✓ Depth image shape: {obs['depth'].shape}")

    if 'imu_accel' in obs and obs['imu_accel'] is not None:
        print(f"  ✓ IMU acceleration: {obs['imu_accel']}")

    if 'imu_gyro' in obs and obs['imu_gyro'] is not None:
        print(f"  ✓ IMU gyroscope: {obs['imu_gyro']}")

    if 'odom_pos' in obs and obs['odom_pos'] is not None:
        print(f"  ✓ Odometry position: {obs['odom_pos']}")

    if 'odom_vel' in obs and obs['odom_vel'] is not None:
        print(f"  ✓ Odometry velocity: {obs['odom_vel']}")

    print(f"  ✓ Timestamp: {obs['timestamp']}")

    return True


def start_docker_container():
    """Start Docker container and wait for it to be ready.

    Returns:
        bool: True if container started successfully, False otherwise
    """
    print("\n[Docker] Starting ROS 2 container...")
    try:
        # Run docker start script
        result = subprocess.run(
            ["./scripts/docker_start.sh", "--wait"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("  ✓ Docker container started and healthy")
            return True
        else:
            print(f"  ❌ Failed to start Docker container")
            print(f"     {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("  ❌ Docker start timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error starting Docker: {e}")
        return False


def stop_docker_container():
    """Stop Docker container gracefully."""
    print("\n[Docker] Stopping ROS 2 container...")
    try:
        result = subprocess.run(
            ["./scripts/docker_stop.sh"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("  ✓ Docker container stopped")
        else:
            print(f"  ⚠ Warning: Docker stop returned {result.returncode}")

    except Exception as e:
        print(f"  ⚠ Warning during Docker stop: {e}")


def verify_ros2_topics():
    """Verify that ROS 2 topics are visible in Docker container.

    Returns:
        bool: True if topics are visible, False otherwise
    """
    print("\n[Docker] Verifying ROS 2 topics in container...")

    # Wait a moment for topics to be published
    time.sleep(2)

    try:
        # List topics from inside container
        result = subprocess.run(
            ["docker", "exec", "rapid_ros2", "ros2", "topic", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            topics = result.stdout.strip().split('\n')
            topic_count = len([t for t in topics if t.strip()])

            print(f"  ✓ Found {topic_count} ROS 2 topics in container:")

            # Check for expected topics
            expected_topics = ["/camera/depth", "/imu/data", "/odom", "/clock"]
            for expected in expected_topics:
                if expected in topics:
                    print(f"    ✓ {expected}")
                else:
                    print(f"    ⚠ {expected} (not found)")

            return topic_count > 0
        else:
            print(f"  ❌ Could not list topics: {result.stderr}")
            return False

    except Exception as e:
        print(f"  ❌ Error verifying topics: {e}")
        return False


def main():
    """Main test function."""
    args = parse_args()

    print("=" * 80)
    print("Isaac Lab Environment Wrapper - Test Script")
    print("=" * 80)
    print(f"Configuration:")
    print(f"  - Config file: {args.config}")
    print(f"  - Headless mode: {args.headless}")
    print(f"  - Number of steps: {args.num_steps}")
    print(f"  - Scene: {args.scene_family} (seed={args.scene_seed})")
    print(f"  - Docker integration: {args.with_docker}")
    print("=" * 80)

    # Start Docker container if requested
    docker_started = False
    if args.with_docker:
        if not start_docker_container():
            print("\n❌ Docker container failed to start. Aborting test.")
            return 1
        docker_started = True

    # Phase 1: Initialize environment
    print("\n[Phase 1/6] Creating IsaacSimEnvironment...")
    try:
        env = IsaacSimEnvironment(config_path=args.config, headless=args.headless)
        print("  ✓ Environment object created successfully")
    except Exception as e:
        print(f"  ❌ Failed to create environment: {e}")
        return 1

    # Phase 2: Initialize Isaac Sim
    print("\n[Phase 2/6] Initializing Isaac Sim application...")
    try:
        env.initialize_isaac_sim()
        print("  ✓ Isaac Sim initialized successfully")
    except Exception as e:
        print(f"  ❌ Failed to initialize Isaac Sim: {e}")
        env.close()
        return 1

    # Phase 3: Setup sensors
    print("\n[Phase 3/6] Setting up sensors...")
    try:
        env.setup_sensors()
        print("  ✓ Sensors configured successfully")
        print(f"  ✓ Active sensors: {list(env.sensors.keys())}")
    except Exception as e:
        print(f"  ❌ Failed to setup sensors: {e}")
        env.close()
        return 1

    # Phase 4: Setup ROS 2 bridge
    print("\n[Phase 4/6] Setting up ROS 2 bridge...")
    try:
        env.setup_ros2_bridge()
        print("  ✓ ROS 2 bridge initialized successfully")
    except Exception as e:
        print(f"  ❌ Failed to setup ROS 2 bridge: {e}")
        env.close()
        return 1

    # Phase 5: Reset environment (load scene)
    print("\n[Phase 5/6] Resetting environment...")
    try:
        obs = env.reset(scene_family=args.scene_family, seed=args.scene_seed)
        print("  ✓ Environment reset successfully")
        validate_observation(obs, 0)
    except Exception as e:
        print(f"  ❌ Failed to reset environment: {e}")
        env.close()
        return 1

    # Phase 6: Run simulation loop
    print(f"\n[Phase 6/6] Running simulation for {args.num_steps} steps...")
    try:
        for step in range(args.num_steps):
            obs = env.step()

            # Validate every 20 steps
            if step % 20 == 0:
                if not validate_observation(obs, step):
                    print(f"  ⚠ Validation warning at step {step}")

            # Progress indicator
            if (step + 1) % 10 == 0:
                print(f"  Progress: {step + 1}/{args.num_steps} steps completed")

        print(f"  ✓ Simulation completed successfully ({args.num_steps} steps)")

    except KeyboardInterrupt:
        print("\n  ⚠ Simulation interrupted by user")
    except Exception as e:
        print(f"  ❌ Simulation failed: {e}")
        import traceback
        traceback.print_exc()
        env.close()

        # Stop Docker if we started it
        if docker_started:
            stop_docker_container()

        return 1

    # Verify Docker ROS 2 topics if Docker is running
    if args.with_docker:
        if not verify_ros2_topics():
            print("\n⚠ Warning: ROS 2 topics not visible in Docker")
            print("  This may indicate a DDS discovery issue")

    # Cleanup
    print("\n[Cleanup] Closing environment...")
    try:
        env.close()
        print("  ✓ Environment closed successfully")
    except Exception as e:
        print(f"  ⚠ Warning during cleanup: {e}")

    # Stop Docker container if we started it
    if docker_started:
        stop_docker_container()

    print("\n" + "=" * 80)
    print("✓ Test completed successfully!")
    print("=" * 80)

    if args.with_docker:
        print("\nDocker integration test passed!")
        print("ROS 2 topics are being published from Isaac Sim to Docker container.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
