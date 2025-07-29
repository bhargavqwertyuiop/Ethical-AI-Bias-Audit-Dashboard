#!/bin/bash

# Ethical AI Bias Audit Dashboard - Build Script
# This script builds and manages the Docker container for the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="ethical-ai-bias-audit"
CONTAINER_NAME="bias-audit-dashboard"
VERSION=${1:-latest}
REGISTRY=${REGISTRY:-""}

echo -e "${BLUE}🛡️  Ethical AI Bias Audit Dashboard - Build Script${NC}"
echo -e "${BLUE}=====================================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    print_status "Docker is available and running"
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image: ${IMAGE_NAME}:${VERSION}"
    
    # Build the image
    docker build \
        --tag ${IMAGE_NAME}:${VERSION} \
        --tag ${IMAGE_NAME}:latest \
        --build-arg VERSION=${VERSION} \
        --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --build-arg VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
        .

    print_status "Image built successfully: ${IMAGE_NAME}:${VERSION}"
}

# Function to run the container
run_container() {
    print_status "Stopping existing container (if any)..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true

    print_status "Starting new container..."
    docker run -d \
        --name ${CONTAINER_NAME} \
        --port 8501:8501 \
        --restart unless-stopped \
        --volume $(pwd)/data:/app/data:ro \
        ${IMAGE_NAME}:${VERSION}

    print_status "Container started successfully"
    print_status "Dashboard available at: http://localhost:8501"
}

# Function to push to registry
push_image() {
    if [ -z "$REGISTRY" ]; then
        print_warning "No registry specified. Skipping push."
        return
    fi

    print_status "Tagging image for registry: ${REGISTRY}"
    docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:${VERSION}
    docker tag ${IMAGE_NAME}:latest ${REGISTRY}/${IMAGE_NAME}:latest

    print_status "Pushing to registry..."
    docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
    docker push ${REGISTRY}/${IMAGE_NAME}:latest

    print_status "Image pushed successfully"
}

# Function to show image information
show_info() {
    print_status "Image Information:"
    docker images | grep ${IMAGE_NAME} || print_warning "No images found"
    
    print_status "Container Information:"
    docker ps -a | grep ${CONTAINER_NAME} || print_warning "No containers found"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    docker image prune -f
    print_status "Cleanup completed"
}

# Function to show logs
show_logs() {
    if docker ps | grep -q ${CONTAINER_NAME}; then
        print_status "Showing container logs..."
        docker logs -f ${CONTAINER_NAME}
    else
        print_error "Container ${CONTAINER_NAME} is not running"
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [VERSION] [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image (default)"
    echo "  run       Build and run the container"
    echo "  push      Build and push to registry"
    echo "  info      Show image and container information"
    echo "  logs      Show container logs"
    echo "  cleanup   Stop container and clean up"
    echo "  help      Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  REGISTRY  Docker registry URL (for push command)"
    echo ""
    echo "Examples:"
    echo "  $0 v1.0.0 build"
    echo "  $0 latest run"
    echo "  REGISTRY=myregistry.com $0 v1.0.0 push"
}

# Main execution
main() {
    local command=${2:-build}

    case $command in
        build)
            check_docker
            build_image
            ;;
        run)
            check_docker
            build_image
            run_container
            ;;
        push)
            check_docker
            build_image
            push_image
            ;;
        info)
            show_info
            ;;
        logs)
            show_logs
            ;;
        cleanup)
            cleanup
            ;;
        help)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"