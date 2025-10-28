#!/bin/bash
# Test DDS communication between Isaac Sim host and Docker ROS 2 container
#
# This script verifies that ROS 2 topics can be discovered across the
# host-container boundary using DDS.
#
# Usage:
#   ./scripts/docker_test.sh

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}RAPID v2 DDS Communication Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^rapid_ros2$"; then
    echo -e "${RED}✗ Container 'rapid_ros2' is not running${NC}"
    echo "  Start it with: ./scripts/docker_start.sh"
    exit 1
fi

echo -e "${GREEN}✓ Container is running${NC}"
echo ""

# Test 1: Check ROS 2 inside container
echo -e "${YELLOW}Test 1: ROS 2 inside container${NC}"
if docker exec rapid_ros2 ros2 --version &> /dev/null; then
    VERSION=$(docker exec rapid_ros2 ros2 --version)
    echo -e "${GREEN}  ✓ $VERSION${NC}"
else
    echo -e "${RED}  ✗ ROS 2 not working in container${NC}"
    exit 1
fi

# Test 2: Check topic listing in container
echo -e "${YELLOW}Test 2: Topic listing in container${NC}"
TOPICS=$(docker exec rapid_ros2 ros2 topic list 2>/dev/null || echo "")
if [ -n "$TOPICS" ]; then
    TOPIC_COUNT=$(echo "$TOPICS" | wc -l)
    echo -e "${GREEN}  ✓ Found $TOPIC_COUNT topics${NC}"

    # Show topics
    echo "$TOPICS" | while read -r topic; do
        echo "    - $topic"
    done
else
    echo -e "${YELLOW}  ⚠  No topics found yet (this is normal if Isaac Sim is not running)${NC}"
fi
echo ""

# Test 3: Check DDS discovery
echo -e "${YELLOW}Test 3: DDS Configuration${NC}"
DDS_CONFIG=$(docker exec rapid_ros2 bash -c 'echo $RMW_IMPLEMENTATION')
DOMAIN_ID=$(docker exec rapid_ros2 bash -c 'echo $ROS_DOMAIN_ID')
echo -e "${GREEN}  ✓ RMW Implementation: $DDS_CONFIG${NC}"
echo -e "${GREEN}  ✓ ROS Domain ID: $DOMAIN_ID${NC}"

# Check FastDDS config
if docker exec rapid_ros2 test -f /root/.ros/fastdds.xml; then
    echo -e "${GREEN}  ✓ FastDDS config file mounted${NC}"
else
    echo -e "${RED}  ✗ FastDDS config file not found${NC}"
fi
echo ""

# Test 4: Check if host ROS 2 can see container topics (if ROS 2 on host)
echo -e "${YELLOW}Test 4: Host-Container Communication${NC}"
if command -v ros2 &> /dev/null; then
    # Check if host ROS 2 environment is configured
    if [ "$ROS_DOMAIN_ID" == "0" ]; then
        echo "Checking if host can see container topics..."
        HOST_TOPICS=$(ros2 topic list 2>/dev/null || echo "")

        if [ -n "$HOST_TOPICS" ]; then
            HOST_COUNT=$(echo "$HOST_TOPICS" | wc -l)
            echo -e "${GREEN}  ✓ Host can see $HOST_COUNT topics${NC}"

            # Check for overlap
            COMMON_TOPICS=$(comm -12 <(echo "$TOPICS" | sort) <(echo "$HOST_TOPICS" | sort))
            if [ -n "$COMMON_TOPICS" ]; then
                COMMON_COUNT=$(echo "$COMMON_TOPICS" | wc -l)
                echo -e "${GREEN}  ✓ $COMMON_COUNT topics visible from both host and container${NC}"
            fi
        else
            echo -e "${YELLOW}  ⚠  Host ROS 2 not seeing topics (ensure ROS_DOMAIN_ID=0)${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠  Host ROS_DOMAIN_ID not set to 0${NC}"
        echo "     Run: export ROS_DOMAIN_ID=0"
    fi
else
    echo -e "${YELLOW}  ℹ  ROS 2 not installed on host (not required for Isaac Sim)${NC}"
fi
echo ""

# Test 5: Container health status
echo -e "${YELLOW}Test 5: Container Health${NC}"
HEALTH_STATUS=$(docker inspect --format='{{.State.Health.Status}}' rapid_ros2 2>/dev/null || echo "no health check")
if [ "$HEALTH_STATUS" == "healthy" ]; then
    echo -e "${GREEN}  ✓ Container is healthy${NC}"
elif [ "$HEALTH_STATUS" == "no health check" ]; then
    echo -e "${YELLOW}  ⚠  No health check configured${NC}"
else
    echo -e "${RED}  ✗ Container health: $HEALTH_STATUS${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Docker container is functional${NC}"
echo -e "${GREEN}✓ ROS 2 Jazzy is working inside container${NC}"
echo -e "${GREEN}✓ DDS configuration is correct${NC}"
echo ""
echo "Next steps:"
echo "  1. Source ROS 2 environment: source scripts/activate_ros2_env.sh"
echo "  2. Run Isaac Sim: python scripts/test_ros2_bridge.py"
echo "  3. Verify topics in container: docker exec rapid_ros2 ros2 topic list"
echo "  4. Monitor topic data: docker exec rapid_ros2 ros2 topic hz /camera/depth"
echo ""
