#!/bin/bash
# ROS 2 Environment Configuration for Isaac Sim
# Source this script before running Isaac Sim with ROS 2 bridge
#
# Usage:
#   source scripts/activate_ros2_env.sh
#
# This script configures the environment to use Isaac Sim's bundled ROS 2 Jazzy
# libraries and sets up DDS for communication with Docker containers.

set -e

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Configuring ROS 2 Environment for Isaac Sim...${NC}"

# ============================================================================
# ROS 2 Configuration
# ============================================================================

export ROS_DISTRO=jazzy
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# Get project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Set FastDDS configuration file
export FASTRTPS_DEFAULT_PROFILES_FILE="${PROJECT_ROOT}/docker/.ros/fastdds.xml"

echo -e "${GREEN}  ✓ ROS_DISTRO=${ROS_DISTRO}${NC}"
echo -e "${GREEN}  ✓ ROS_DOMAIN_ID=${ROS_DOMAIN_ID}${NC}"
echo -e "${GREEN}  ✓ RMW_IMPLEMENTATION=${RMW_IMPLEMENTATION}${NC}"
echo -e "${GREEN}  ✓ FASTRTPS_DEFAULT_PROFILES_FILE=${FASTRTPS_DEFAULT_PROFILES_FILE}${NC}"

# ============================================================================
# Isaac Sim ROS 2 Bridge Configuration
# ============================================================================

# Check if running in conda environment
if [ -z "$CONDA_PREFIX" ]; then
    echo -e "${YELLOW}⚠  Warning: Not in a conda environment${NC}"
    echo -e "${YELLOW}   Run: conda activate env_isaaclab${NC}"
    return 1
fi

# Path to Isaac Sim's bundled ROS 2 Jazzy libraries
ISAAC_ROS2_BASE="${CONDA_PREFIX}/lib/python3.11/site-packages/isaacsim/exts/isaacsim.ros2.bridge/jazzy"

if [ -d "$ISAAC_ROS2_BASE" ]; then
    # Add ROS 2 libraries to LD_LIBRARY_PATH
    export LD_LIBRARY_PATH="${ISAAC_ROS2_BASE}/lib:${LD_LIBRARY_PATH}"

    # Add ROS 2 Python packages to PYTHONPATH
    export PYTHONPATH="${ISAAC_ROS2_BASE}/rclpy:${PYTHONPATH}"

    echo -e "${GREEN}  ✓ Isaac Sim ROS 2 Jazzy libraries configured${NC}"
    echo -e "${GREEN}    Path: ${ISAAC_ROS2_BASE}${NC}"
else
    echo -e "${YELLOW}⚠  Warning: Isaac Sim ROS 2 bridge not found${NC}"
    echo -e "${YELLOW}   Expected path: ${ISAAC_ROS2_BASE}${NC}"
    echo -e "${YELLOW}   ROS 2 bridge may not work. Check Isaac Sim installation.${NC}"
fi

# ============================================================================
# Verification
# ============================================================================

echo ""
echo -e "${GREEN}ROS 2 Environment Configured Successfully!${NC}"
echo ""
echo "Environment Summary:"
echo "  ROS Distribution: ${ROS_DISTRO}"
echo "  Domain ID: ${ROS_DOMAIN_ID}"
echo "  Middleware: ${RMW_IMPLEMENTATION}"
echo "  FastDDS Config: ${FASTRTPS_DEFAULT_PROFILES_FILE}"
echo "  Isaac ROS 2 Path: ${ISAAC_ROS2_BASE}"
echo ""
echo "Next steps:"
echo "  1. Start Docker container: docker compose up -d"
echo "  2. Run Isaac Sim script: python scripts/test_ros2_bridge.py"
echo "  3. Verify topics: ros2 topic list"
echo ""
