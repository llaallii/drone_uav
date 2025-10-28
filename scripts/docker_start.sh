#!/bin/bash
# Start Docker ROS 2 container for RAPID v2
#
# Usage:
#   ./scripts/docker_start.sh          # Start in background
#   ./scripts/docker_start.sh --wait   # Start and wait for health check

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting RAPID v2 ROS 2 Docker Container...${NC}"

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Error: Docker is not installed${NC}"
    echo "  Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}✗ Error: Docker daemon is not running${NC}"
    echo "  Please start Docker"
    exit 1
fi

# Check if container is already running
if docker ps --format '{{.Names}}' | grep -q "^rapid_ros2$"; then
    echo -e "${YELLOW}⚠  Container 'rapid_ros2' is already running${NC}"
    docker ps --filter "name=rapid_ros2" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    exit 0
fi

# Build image if it doesn't exist
if ! docker images --format '{{.Repository}}' | grep -q "drone_uav-rapid_ros2"; then
    echo -e "${YELLOW}Building Docker image (first time only)...${NC}"
    docker compose build
fi

# Start container
echo "Starting container..."
docker compose up -d

# Wait for health check if requested
if [[ "$1" == "--wait" ]]; then
    echo -e "${YELLOW}Waiting for container to be healthy...${NC}"

    MAX_WAIT=30
    COUNTER=0
    until [ "$(docker inspect --format='{{.State.Health.Status}}' rapid_ros2 2>/dev/null)" == "healthy" ]; do
        sleep 1
        COUNTER=$((COUNTER + 1))
        if [ $COUNTER -ge $MAX_WAIT ]; then
            echo -e "${RED}✗ Container failed to become healthy after ${MAX_WAIT}s${NC}"
            echo "Container logs:"
            docker logs rapid_ros2 --tail 50
            exit 1
        fi
        echo -n "."
    done
    echo ""
    echo -e "${GREEN}✓ Container is healthy${NC}"
fi

echo ""
echo -e "${GREEN}✓ ROS 2 container started successfully${NC}"
echo ""
echo "Container status:"
docker ps --filter "name=rapid_ros2" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f rapid_ros2          # View logs"
echo "  docker exec -it rapid_ros2 bash            # Enter container"
echo "  docker exec rapid_ros2 ros2 topic list     # List ROS 2 topics"
echo "  ./scripts/docker_stop.sh                   # Stop container"
echo ""
