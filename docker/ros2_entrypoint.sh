#!/bin/bash
# Entrypoint script for RAPID v2 ROS 2 container
# This script sources the ROS 2 environment and sets up DDS configuration

set -e

# Source ROS 2 setup
source /opt/ros/jazzy/setup.bash

# Set ROS 2 environment variables
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
export RMW_IMPLEMENTATION=${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}

# Set FastDDS configuration if provided
if [ -f "/root/.ros/fastdds.xml" ]; then
    export FASTRTPS_DEFAULT_PROFILES_FILE=/root/.ros/fastdds.xml
    echo "[ROS2 Container] Using FastDDS config: $FASTRTPS_DEFAULT_PROFILES_FILE"
fi

echo "[ROS2 Container] ROS 2 environment configured:"
echo "  ROS_DISTRO: $ROS_DISTRO"
echo "  ROS_DOMAIN_ID: $ROS_DOMAIN_ID"
echo "  RMW_IMPLEMENTATION: $RMW_IMPLEMENTATION"

# Execute the command
exec "$@"
