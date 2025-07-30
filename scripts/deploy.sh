#!/bin/bash

# Ethical AI Bias Audit Dashboard - Deployment Script
# This script deploys the application to different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-development}
IMAGE_NAME="ethical-ai-bias-audit"
COMPOSE_FILE=""

echo -e "${BLUE}🛡️  Ethical AI Bias Audit Dashboard - Deployment Script${NC}"
echo -e "${BLUE}==========================================================${NC}"

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

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_status "Prerequisites check passed"
}

# Function to set environment configuration
set_environment() {
    case $ENVIRONMENT in
        development|dev)
            print_status "Deploying to DEVELOPMENT environment"
            COMPOSE_FILE="docker-compose.yml"
            ;;
        staging)
            print_status "Deploying to STAGING environment"
            COMPOSE_FILE="docker-compose.yml"
            export STREAMLIT_SERVER_PORT=8502
            ;;
        production|prod)
            print_status "Deploying to PRODUCTION environment"
            COMPOSE_FILE="docker-compose.yml --profile production"
            check_production_requirements
            ;;
        *)
            print_error "Unknown environment: $ENVIRONMENT"
            print_status "Valid environments: development, staging, production"
            exit 1
            ;;
    esac
}

# Function to check production requirements
check_production_requirements() {
    print_status "Checking production requirements..."

    # Check for SSL certificates
    if [ ! -d "ssl" ] || [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        print_warning "SSL certificates not found in ./ssl/ directory"
        print_status "Generating self-signed certificates for testing..."
        
        mkdir -p ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
            2>/dev/null || print_warning "Failed to generate SSL certificates"
    fi

    # Check environment variables
    if [ -z "$REGISTRY" ]; then
        print_warning "REGISTRY environment variable not set. Using local image."
    fi
}

# Function to build and deploy
deploy() {
    print_status "Starting deployment..."

    # Pull latest images if using registry
    if [ ! -z "$REGISTRY" ]; then
        print_status "Pulling latest images from registry..."
        docker-compose -f $COMPOSE_FILE pull || print_warning "Failed to pull some images"
    fi

    # Build and start services
    print_status "Building and starting services..."
    docker-compose -f $COMPOSE_FILE up -d --build

    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10

    # Check service health
    check_health
}

# Function to check service health
check_health() {
    print_status "Checking service health..."

    local retries=30
    local wait_time=2

    for i in $(seq 1 $retries); do
        if curl -f http://localhost:8501/_stcore/health &>/dev/null; then
            print_status "✅ Application is healthy and ready!"
            show_access_info
            return 0
        fi
        
        print_status "Waiting for application to be ready... ($i/$retries)"
        sleep $wait_time
    done

    print_error "❌ Application failed to become healthy within expected time"
    print_status "Checking logs..."
    docker-compose -f $COMPOSE_FILE logs --tail=20
    return 1
}

# Function to show access information
show_access_info() {
    print_status "🎉 Deployment completed successfully!"
    echo ""
    print_status "Access Information:"
    
    case $ENVIRONMENT in
        development|dev)
            echo -e "  📊 Dashboard: ${GREEN}http://localhost:8501${NC}"
            ;;
        staging)
            echo -e "  📊 Dashboard: ${GREEN}http://localhost:8502${NC}"
            ;;
        production|prod)
            echo -e "  📊 Dashboard: ${GREEN}https://localhost${NC}"
            echo -e "  🔒 HTTP Redirect: ${GREEN}http://localhost${NC} → https://localhost"
            ;;
    esac
    
    echo ""
    print_status "Useful Commands:"
    echo "  View logs:    docker-compose -f $COMPOSE_FILE logs -f"
    echo "  Stop services: docker-compose -f $COMPOSE_FILE down"
    echo "  Restart:      docker-compose -f $COMPOSE_FILE restart"
    echo "  Status:       docker-compose -f $COMPOSE_FILE ps"
}

# Function to stop deployment
stop_deployment() {
    print_status "Stopping deployment..."
    docker-compose -f $COMPOSE_FILE down
    print_status "Deployment stopped"
}

# Function to show logs
show_logs() {
    print_status "Showing application logs..."
    docker-compose -f $COMPOSE_FILE logs -f
}

# Function to show status
show_status() {
    print_status "Service Status:"
    docker-compose -f $COMPOSE_FILE ps
    
    print_status "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

# Function to update deployment
update_deployment() {
    print_status "Updating deployment..."
    
    # Pull latest images
    if [ ! -z "$REGISTRY" ]; then
        docker-compose -f $COMPOSE_FILE pull
    fi
    
    # Recreate containers with new images
    docker-compose -f $COMPOSE_FILE up -d --force-recreate
    
    check_health
}

# Function to backup data
backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    print_status "Creating backup in $backup_dir..."
    
    mkdir -p "$backup_dir"
    
    # Backup data directory
    if [ -d "data" ]; then
        cp -r data "$backup_dir/"
    fi
    
    # Backup uploaded files
    if docker volume inspect uploads_data &>/dev/null; then
        docker run --rm -v uploads_data:/data -v $(pwd)/$backup_dir:/backup alpine \
            tar czf /backup/uploads.tar.gz -C /data .
    fi
    
    print_status "Backup completed: $backup_dir"
}

# Function to show help
show_help() {
    echo "Usage: $0 [ENVIRONMENT] [COMMAND]"
    echo ""
    echo "Environments:"
    echo "  development   Deploy to development environment (default)"
    echo "  staging       Deploy to staging environment"
    echo "  production    Deploy to production environment with SSL"
    echo ""
    echo "Commands:"
    echo "  deploy        Deploy the application (default)"
    echo "  stop          Stop the deployment"
    echo "  status        Show deployment status"
    echo "  logs          Show application logs"
    echo "  update        Update deployment with latest images"
    echo "  backup        Backup application data"
    echo "  help          Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  REGISTRY      Docker registry URL"
    echo ""
    echo "Examples:"
    echo "  $0 development deploy"
    echo "  $0 production deploy"
    echo "  $0 staging logs"
    echo "  REGISTRY=myregistry.com $0 production update"
}

# Main execution
main() {
    local command=${2:-deploy}

    # Set environment configuration
    set_environment

    case $command in
        deploy)
            check_prerequisites
            deploy
            ;;
        stop)
            stop_deployment
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        update)
            check_prerequisites
            update_deployment
            ;;
        backup)
            backup_data
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