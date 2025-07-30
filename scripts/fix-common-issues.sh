#!/bin/bash

# Ethical AI Bias Audit Dashboard - Issue Fix Script
# This script automatically fixes common issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️  Ethical AI Bias Audit Dashboard - Issue Fix Script${NC}"
echo -e "${BLUE}======================================================${NC}"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to fix Streamlit experimental_rerun issue
fix_streamlit_issue() {
    print_status "Checking for Streamlit experimental_rerun issue..."
    
    if grep -q "experimental_rerun" dashboard.py; then
        print_warning "Found experimental_rerun in dashboard.py"
        print_status "Fixing experimental_rerun -> rerun..."
        
        # Create backup
        cp dashboard.py dashboard.py.backup
        
        # Fix the issue
        sed -i 's/st\.experimental_rerun()/st.rerun()/g' dashboard.py
        
        print_status "✅ Fixed experimental_rerun issue"
    else
        print_status "✅ No experimental_rerun issues found"
    fi
}

# Function to update Streamlit version
update_streamlit() {
    print_status "Checking Streamlit version..."
    
    if command -v pip &> /dev/null; then
        current_version=$(pip show streamlit 2>/dev/null | grep Version | cut -d' ' -f2 || echo "not installed")
        print_status "Current Streamlit version: $current_version"
        
        if [[ "$current_version" == "not installed" ]]; then
            print_status "Installing Streamlit..."
            pip install streamlit>=1.28.0
        else
            print_status "Upgrading Streamlit..."
            pip install --upgrade streamlit>=1.28.0
        fi
        
        print_status "✅ Streamlit updated"
    else
        print_warning "pip not found, skipping Streamlit update"
    fi
}

# Function to fix Docker issues
fix_docker_issues() {
    print_status "Checking Docker setup..."
    
    if command -v docker &> /dev/null; then
        print_status "Docker is available"
        
        # Stop and remove existing containers
        print_status "Stopping existing containers..."
        docker stop bias-audit-dashboard 2>/dev/null || true
        docker rm bias-audit-dashboard 2>/dev/null || true
        
        # Remove old images
        print_status "Removing old images..."
        docker rmi ethical-ai-bias-audit:latest 2>/dev/null || true
        
        # Clean up Docker system
        print_status "Cleaning up Docker system..."
        docker system prune -f
        
        print_status "✅ Docker cleanup completed"
    else
        print_warning "Docker not found, skipping Docker fixes"
    fi
}

# Function to rebuild application
rebuild_application() {
    print_status "Rebuilding application..."
    
    if [ -f "docker-compose.yml" ]; then
        print_status "Using Docker Compose..."
        docker-compose down || true
        docker-compose build --no-cache
        docker-compose up -d
        
        print_status "✅ Application rebuilt with Docker Compose"
    elif [ -f "Dockerfile" ]; then
        print_status "Using Docker..."
        docker build -t ethical-ai-bias-audit:latest --no-cache .
        
        print_status "✅ Docker image rebuilt"
    else
        print_warning "No Docker files found, skipping rebuild"
    fi
}

# Function to test application
test_application() {
    print_status "Testing application..."
    
    if [ -f "test_app.py" ]; then
        python test_app.py
        if [ $? -eq 0 ]; then
            print_status "✅ Application tests passed"
        else
            print_error "❌ Application tests failed"
            return 1
        fi
    else
        print_warning "test_app.py not found, skipping tests"
    fi
}

# Function to check permissions
fix_permissions() {
    print_status "Checking file permissions..."
    
    # Make scripts executable
    if [ -d "scripts" ]; then
        chmod +x scripts/*.sh 2>/dev/null || true
        print_status "✅ Script permissions fixed"
    fi
    
    # Fix data directory permissions
    if [ -d "data" ]; then
        chmod -R 644 data/* 2>/dev/null || true
        print_status "✅ Data permissions fixed"
    fi
}

# Function to verify sample data
verify_sample_data() {
    print_status "Verifying sample data..."
    
    if [ -f "data/sample_hiring_data.csv" ]; then
        # Check if file is readable
        if head -n 1 "data/sample_hiring_data.csv" >/dev/null 2>&1; then
            lines=$(wc -l < "data/sample_hiring_data.csv")
            print_status "✅ Sample data verified: $lines lines"
        else
            print_error "❌ Sample data file is corrupted"
            return 1
        fi
    else
        print_error "❌ Sample data file missing"
        return 1
    fi
}

# Main execution
main() {
    local fix_type=${1:-all}
    
    case $fix_type in
        streamlit)
            fix_streamlit_issue
            update_streamlit
            ;;
        docker)
            fix_docker_issues
            rebuild_application
            ;;
        permissions)
            fix_permissions
            ;;
        data)
            verify_sample_data
            ;;
        test)
            test_application
            ;;
        all)
            print_status "Running all fixes..."
            fix_permissions
            verify_sample_data
            fix_streamlit_issue
            update_streamlit
            fix_docker_issues
            test_application
            print_status "🎉 All fixes completed!"
            ;;
        *)
            echo "Usage: $0 [streamlit|docker|permissions|data|test|all]"
            echo ""
            echo "Available fixes:"
            echo "  streamlit     Fix Streamlit experimental_rerun issues"
            echo "  docker        Fix Docker-related issues"
            echo "  permissions   Fix file permissions"
            echo "  data          Verify sample data"
            echo "  test          Run application tests"
            echo "  all           Run all fixes (default)"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"