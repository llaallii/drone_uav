#!/bin/bash
# Stop Docker ROS 2 container for RAPID v2
#
# Usage:
#   ./scripts/docker_stop.sh           # Stop gracefully
#   ./scripts/docker_stop.sh --force   # Force stop

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Stopping RAPID v2 ROS 2 Docker Container...${NC}"

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^rapid_ros2$"; then
    echo -e "${YELLOW}⚠  Container 'rapid_ros2' is not running${NC}"
    exit 0
fi

# Stop container
if [[ "$1" == "--force" ]]; then
    echo "Force stopping container..."
    docker compose kill
else
    echo "Stopping container gracefully..."
    docker compose stop
fi

echo -e "${GREEN}✓ Container stopped${NC}"
echo ""
echo "To start again: ./scripts/docker_start.sh"
echo "To remove container: docker compose down"
echo ""
