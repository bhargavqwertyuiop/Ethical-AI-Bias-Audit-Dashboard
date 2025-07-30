# 🐳 Docker Deployment Guide

This guide provides comprehensive instructions for deploying the Ethical AI Bias Audit Dashboard using Docker.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Building the Image](#building-the-image)
4. [Running the Container](#running-the-container)
5. [Docker Compose Deployment](#docker-compose-deployment)
6. [Production Deployment](#production-deployment)
7. [Configuration](#configuration)
8. [Monitoring & Logging](#monitoring--logging)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ethical-ai-bias-audit-dashboard

# Deploy with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8501
```

### Option 2: Using Build Scripts

```bash
# Build and run using the provided script
./scripts/build.sh latest run

# Access the application
open http://localhost:8501
```

### Option 3: Manual Docker Commands

```bash
# Build the image
docker build -t ethical-ai-bias-audit .

# Run the container
docker run -d \
  --name bias-audit-dashboard \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data:ro \
  ethical-ai-bias-audit

# Access the application
open http://localhost:8501
```

## 📋 Prerequisites

### Required Software

- **Docker**: Version 20.10+ recommended
- **Docker Compose**: Version 2.0+ recommended
- **Git**: For cloning the repository

### System Requirements

- **Memory**: Minimum 2GB RAM, 4GB+ recommended
- **Storage**: At least 2GB free space
- **CPU**: 2+ cores recommended for optimal performance
- **Network**: Port 8501 available (or alternative port)

### Installation

#### Docker Installation

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
# Install Docker Desktop from https://docker.com/products/docker-desktop
# Or using Homebrew
brew install --cask docker
```

**Windows:**
Download and install Docker Desktop from https://docker.com/products/docker-desktop

#### Docker Compose Installation

```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# macOS/Windows (included with Docker Desktop)
```

## 🏗️ Building the Image

### Manual Build

```bash
# Basic build
docker build -t ethical-ai-bias-audit .

# Build with specific version
docker build -t ethical-ai-bias-audit:v1.0.0 .

# Build with build arguments
docker build \
  --build-arg VERSION=v1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t ethical-ai-bias-audit:v1.0.0 .
```

### Using Build Script

```bash
# Basic build
./scripts/build.sh

# Build specific version
./scripts/build.sh v1.0.0

# Build and run
./scripts/build.sh latest run

# Push to registry
REGISTRY=myregistry.com ./scripts/build.sh v1.0.0 push
```

### Build Options

| Build Argument | Description | Default |
|----------------|-------------|---------|
| `VERSION` | Application version | `latest` |
| `BUILD_DATE` | Build timestamp | Current time |
| `VCS_REF` | Git commit hash | `unknown` |

## 🏃 Running the Container

### Basic Run

```bash
docker run -d \
  --name bias-audit-dashboard \
  -p 8501:8501 \
  ethical-ai-bias-audit
```

### Run with Volumes

```bash
docker run -d \
  --name bias-audit-dashboard \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data:ro \
  -v uploads:/app/uploads \
  ethical-ai-bias-audit
```

### Run with Environment Variables

```bash
docker run -d \
  --name bias-audit-dashboard \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  -v $(pwd)/data:/app/data:ro \
  ethical-ai-bias-audit
```

### Run with Custom Configuration

```bash
docker run -d \
  --name bias-audit-dashboard \
  -p 8501:8501 \
  -v $(pwd)/.streamlit/config.toml:/app/.streamlit/config.toml:ro \
  -v $(pwd)/data:/app/data:ro \
  ethical-ai-bias-audit
```

## 🐳 Docker Compose Deployment

### Development Environment

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Staging Environment

```bash
# Deploy to staging
./scripts/deploy.sh staging deploy

# Check status
./scripts/deploy.sh staging status

# View logs
./scripts/deploy.sh staging logs
```

### Service Configuration

The `docker-compose.yml` includes:

- **bias-audit-dashboard**: Main application service
- **nginx**: Reverse proxy (production only)
- **uploads_data**: Persistent volume for uploads
- **bias-audit-network**: Custom network

### Docker Compose Commands

```bash
# Build and start services
docker-compose up -d --build

# Scale the application
docker-compose up -d --scale bias-audit-dashboard=3

# Update services
docker-compose pull
docker-compose up -d

# View service status
docker-compose ps

# Execute commands in container
docker-compose exec bias-audit-dashboard bash

# View resource usage
docker-compose top
```

## 🏭 Production Deployment

### Production Setup

```bash
# Deploy to production
./scripts/deploy.sh production deploy
```

### Production Features

- **SSL/TLS**: HTTPS encryption with certificate management
- **Reverse Proxy**: Nginx for load balancing and security
- **Security Headers**: Enhanced security configuration
- **Rate Limiting**: API rate limiting protection
- **Health Checks**: Automated health monitoring
- **Gzip Compression**: Optimized content delivery

### SSL Certificate Setup

#### Option 1: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot

# Generate certificates
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*.pem
```

#### Option 2: Self-Signed Certificates

```bash
# Generate self-signed certificates
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

### Environment Variables for Production

```bash
export REGISTRY=your-registry.com
export DOMAIN=yourdomain.com
export SSL_EMAIL=admin@yourdomain.com
```

## ⚙️ Configuration

### Streamlit Configuration

Edit `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
maxUploadSize = 200

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Server port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Server address | `0.0.0.0` |
| `STREAMLIT_SERVER_HEADLESS` | Headless mode | `true` |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Usage stats | `false` |

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./data` | `/app/data` | Sample datasets (read-only) |
| `uploads_data` | `/app/uploads` | User uploads (persistent) |
| `./.streamlit/config.toml` | `/app/.streamlit/config.toml` | Configuration |

## 📊 Monitoring & Logging

### Health Checks

```bash
# Manual health check
curl -f http://localhost:8501/_stcore/health

# Docker health check
docker inspect --format='{{.State.Health.Status}}' bias-audit-dashboard
```

### Viewing Logs

```bash
# View application logs
docker logs bias-audit-dashboard

# Follow logs in real-time
docker logs -f bias-audit-dashboard

# View logs with timestamps
docker logs -t bias-audit-dashboard

# View last 100 lines
docker logs --tail=100 bias-audit-dashboard
```

### Resource Monitoring

```bash
# View resource usage
docker stats bias-audit-dashboard

# View detailed container info
docker inspect bias-audit-dashboard

# View process list
docker exec bias-audit-dashboard ps aux
```

### Log Management

For production environments, consider:

- **Log Rotation**: Configure log rotation to prevent disk space issues
- **Centralized Logging**: Use ELK stack or similar for log aggregation
- **Monitoring**: Set up monitoring with Prometheus/Grafana

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8501

# Use a different port
docker run -d -p 8502:8501 ethical-ai-bias-audit
```

#### Permission Denied

```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
# Logout and login again

# Fix file permissions
sudo chown -R $USER:$USER .
```

#### Container Won't Start

```bash
# Check container logs
docker logs bias-audit-dashboard

# Check container status
docker ps -a

# Inspect container configuration
docker inspect bias-audit-dashboard
```

#### Streamlit AttributeError: 'experimental_rerun'

If you see an error about `st.experimental_rerun()`, this is due to deprecated Streamlit functions:

```bash
# Solution 1: Rebuild with latest image
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Solution 2: Update Streamlit version
pip install --upgrade streamlit>=1.28.0
```

#### Sample Data Loading Issues

```bash
# Test the application components
python test_app.py

# Check if sample data exists
ls -la data/

# Verify CSV format
head data/sample_hiring_data.csv
```

#### Out of Memory

```bash
# Check memory usage
docker stats

# Increase memory limit
docker run -d --memory=4g ethical-ai-bias-audit
```

### Debugging Commands

```bash
# Access container shell
docker exec -it bias-audit-dashboard bash

# Run container interactively
docker run -it --rm ethical-ai-bias-audit bash

# Check Python packages
docker exec bias-audit-dashboard pip list

# Test Streamlit directly
docker exec bias-audit-dashboard streamlit hello
```

### Performance Tuning

```bash
# Allocate more resources
docker run -d \
  --cpus="2.0" \
  --memory="4g" \
  -p 8501:8501 \
  ethical-ai-bias-audit

# Use Docker Compose with resource limits
version: '3.8'
services:
  bias-audit-dashboard:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## 🚀 Advanced Usage

### Multi-Stage Builds

```dockerfile
# Example multi-stage build for smaller production images
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
WORKDIR /app
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "dashboard.py"]
```

### Custom Networking

```bash
# Create custom network
docker network create bias-audit-net

# Run with custom network
docker run -d \
  --name bias-audit-dashboard \
  --network bias-audit-net \
  -p 8501:8501 \
  ethical-ai-bias-audit
```

### Secrets Management

```bash
# Using Docker secrets (Swarm mode)
echo "my-secret-value" | docker secret create my-secret -

# Mount secret in container
docker service create \
  --name bias-audit-dashboard \
  --secret my-secret \
  --publish 8501:8501 \
  ethical-ai-bias-audit
```

### Container Registry

```bash
# Tag for registry
docker tag ethical-ai-bias-audit:latest myregistry.com/ethical-ai-bias-audit:latest

# Push to registry
docker push myregistry.com/ethical-ai-bias-audit:latest

# Pull from registry
docker pull myregistry.com/ethical-ai-bias-audit:latest
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bias-audit-dashboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bias-audit-dashboard
  template:
    metadata:
      labels:
        app: bias-audit-dashboard
    spec:
      containers:
      - name: dashboard
        image: ethical-ai-bias-audit:latest
        ports:
        - containerPort: 8501
        resources:
          limits:
            memory: "4Gi"
            cpu: "2"
          requests:
            memory: "2Gi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: bias-audit-service
spec:
  selector:
    app: bias-audit-dashboard
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Streamlit in Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Production Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review container logs: `docker logs bias-audit-dashboard`
3. Check our [GitHub Issues](https://github.com/your-repo/issues)
4. Join our [Community Discussions](https://github.com/your-repo/discussions)

---

**Happy Deploying! 🚀**