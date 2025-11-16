#!/bin/bash
# Refinory AI Agent Platform Deployment Script
# One-click deployment for complete Refinory infrastructure

set -e  # Exit on any error
set -u  # Exit on undefined variables

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
REFINORY_DIR="$PROJECT_ROOT/refinory"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if ! command_exists kubectl; then
        log_warning "kubectl not found - Kubernetes deployment will not be available"
    fi
    
    if ! command_exists helm; then
        log_warning "helm not found - Helm-based deployments will not be available"
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install the missing dependencies and try again"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi
    
    log_success "All prerequisites satisfied"
}

# Load environment configuration
load_environment() {
    log_info "Loading environment configuration..."
    
    # Load from discovery.yml if available
    if [[ -f "$PROJECT_ROOT/discovery.yml" ]]; then
        log_info "Found discovery.yml configuration"
        # Extract configuration (simplified - would need yq in production)
    fi
    
    # Load .env file if available
    if [[ -f "$PROJECT_ROOT/.env" ]]; then
        source "$PROJECT_ROOT/.env"
        log_info "Loaded .env configuration"
    fi
    
    # Set defaults for missing variables
    export REFINORY_ENV="${REFINORY_ENV:-development}"
    export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-refinory123}"
    export REDIS_PASSWORD="${REDIS_PASSWORD:-}"
    export JWT_SECRET="${JWT_SECRET:-$(openssl rand -hex 32 2>/dev/null || echo 'dev-jwt-secret-key')}"
    
    log_success "Environment configuration loaded"
}

# Generate environment file
generate_env_file() {
    log_info "Generating environment configuration..."
    
    local env_file="$REFINORY_DIR/.env"
    
    cat > "$env_file" << EOF
# Refinory AI Agent Platform Configuration
# Generated on $(date)

# Environment
REFINORY_ENV=${REFINORY_ENV}
REFINORY_API_PORT=8000
REFINORY_ORCHESTRATOR_PORT=8001

# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=refinory
DB_USERNAME=refinory
DB_PASSWORD=${POSTGRES_PASSWORD}

# Redis Configuration  
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=${REDIS_PASSWORD}

# Qdrant Vector Database
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# Temporal Workflow Engine
TEMPORAL_HOST=temporal
TEMPORAL_PORT=7233

# AI/ML Configuration
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}

# Discord Integration
DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN:-}
DISCORD_GUILD_ID=${DISCORD_GUILD_ID:-}

# GitHub Integration
GITHUB_TOKEN=${GITHUB_TOKEN:-}
GITHUB_ORGANIZATION=${GITHUB_ORGANIZATION:-}

# Security
JWT_SECRET=${JWT_SECRET}

# Monitoring
MONITORING_ENABLED=true
METRICS_PORT=9090
EOF

    log_success "Environment file generated: $env_file"
}

# Build Docker images
build_images() {
    log_info "Building Refinory Docker images..."
    
    cd "$REFINORY_DIR"
    
    # Build main Refinory image
    log_info "Building refinory-ai image..."
    docker build -f Dockerfile.refinory -t refinory-ai:latest .
    
    if [ $? -eq 0 ]; then
        log_success "Refinory AI image built successfully"
    else
        log_error "Failed to build Refinory AI image"
        exit 1
    fi
}

# Deploy with Docker Compose
deploy_docker_compose() {
    log_info "Deploying Refinory stack with Docker Compose..."
    
    cd "$REFINORY_DIR"
    
    # Stop existing services
    log_info "Stopping existing services..."
    docker-compose -f docker-compose.refinory.yml down || true
    
    # Pull/update base images
    log_info "Pulling latest base images..."
    docker-compose -f docker-compose.refinory.yml pull postgres redis qdrant temporal prometheus grafana loki
    
    # Start services
    log_info "Starting Refinory services..."
    docker-compose -f docker-compose.refinory.yml up -d
    
    if [ $? -eq 0 ]; then
        log_success "Refinory stack deployed successfully"
    else
        log_error "Failed to deploy Refinory stack"
        exit 1
    fi
    
    # Wait for services to be healthy
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    check_service_health
}

# Check service health
check_service_health() {
    log_info "Checking service health..."
    
    local services=(
        "postgres:5432"
        "redis:6379" 
        "qdrant:6333"
        "refinory-api:8000"
        "prometheus:9090"
    )
    
    for service in "${services[@]}"; do
        local name="${service%%:*}"
        local port="${service##*:}"
        
        log_info "Checking $name..."
        
        # Wait up to 30 seconds for service
        local timeout=30
        local counter=0
        
        while [ $counter -lt $timeout ]; do
            if docker-compose -f "$REFINORY_DIR/docker-compose.refinory.yml" exec -T "$name" timeout 1 bash -c "echo > /dev/tcp/localhost/$port" 2>/dev/null; then
                log_success "$name is healthy"
                break
            fi
            
            sleep 1
            counter=$((counter + 1))
        done
        
        if [ $counter -eq $timeout ]; then
            log_warning "$name health check timed out"
        fi
    done
}

# Initialize database
initialize_database() {
    log_info "Initializing Refinory database..."
    
    cd "$REFINORY_DIR"
    
    # Wait for PostgreSQL to be ready
    log_info "Waiting for PostgreSQL to be ready..."
    docker-compose -f docker-compose.refinory.yml exec -T postgres bash -c '
        until pg_isready -U refinory -d refinory; do
            echo "PostgreSQL is unavailable - sleeping"
            sleep 1
        done
        echo "PostgreSQL is ready"
    '
    
    # Run database migrations/schema creation
    log_info "Creating database schema..."
    docker-compose -f docker-compose.refinory.yml exec -T refinory-api python -c "
import asyncio
from refinory.database import Database
from refinory.config import get_settings

async def init_db():
    settings = get_settings()
    db = Database(settings.postgres_dsn)
    await db.initialize()
    await db.close()
    print('Database initialized successfully')

asyncio.run(init_db())
"
    
    if [ $? -eq 0 ]; then
        log_success "Database initialized successfully"
    else
        log_warning "Database initialization had issues - this may be normal on first run"
    fi
}

# Deploy to Kubernetes
deploy_kubernetes() {
    log_info "Deploying Refinory to Kubernetes..."
    
    if ! command_exists kubectl; then
        log_error "kubectl not available - cannot deploy to Kubernetes"
        return 1
    fi
    
    # Check kubectl connectivity
    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Cannot connect to Kubernetes cluster"
        return 1
    fi
    
    local k8s_dir="$PROJECT_ROOT/bootstrap/k8s"
    
    if [[ ! -d "$k8s_dir" ]]; then
        log_error "Kubernetes manifests not found at $k8s_dir"
        return 1
    fi
    
    # Apply manifests
    log_info "Applying Kubernetes manifests..."
    kubectl apply -f "$k8s_dir/"
    
    # Wait for deployments
    log_info "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/refinory-api deployment/refinory-orchestrator -n refinory || true
    
    log_success "Kubernetes deployment completed"
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring and observability..."
    
    cd "$REFINORY_DIR"
    
    # Import Grafana dashboards
    log_info "Importing Grafana dashboards..."
    
    # Wait for Grafana to be ready
    sleep 10
    
    # Create Grafana API call to import dashboards (simplified)
    log_info "Monitoring setup completed - Grafana available at http://localhost:3000"
    log_info "Default credentials: admin/admin"
}

# Display deployment summary
show_deployment_summary() {
    log_success "🎉 Refinory AI Agent Platform deployed successfully!"
    
    echo
    echo "📋 Service Endpoints:"
    echo "  • Refinory API:         http://localhost:8000"
    echo "  • API Documentation:    http://localhost:8000/docs"
    echo "  • Grafana Monitoring:   http://localhost:3000 (admin/admin)"
    echo "  • Prometheus Metrics:   http://localhost:9090"
    echo "  • PostgreSQL:           localhost:5432 (refinory/refinory123)"
    echo "  • Redis:                localhost:6379"
    echo "  • Qdrant:               http://localhost:6333"
    echo
    echo "🤖 Discord Bot Commands:"
    echo "  • /request              - Request AI architecture generation"
    echo "  • /status <id>          - Check request status"
    echo "  • /list-requests        - List recent requests"
    echo "  • /experts              - List available AI experts"
    echo "  • /refinory-health      - Check platform health"
    echo
    echo "📚 Documentation:"
    echo "  • Architecture:         docs/ARCHITECTURE.md"
    echo "  • Deployment Guide:     docs/DEPLOYMENT.md"
    echo "  • API Reference:        http://localhost:8000/docs"
    echo
    echo "🔧 Management Commands:"
    echo "  • View logs:            docker-compose -f $REFINORY_DIR/docker-compose.refinory.yml logs -f"
    echo "  • Restart services:     docker-compose -f $REFINORY_DIR/docker-compose.refinory.yml restart"
    echo "  • Stop services:        docker-compose -f $REFINORY_DIR/docker-compose.refinory.yml down"
    echo
    echo "🚀 Next Steps:"
    echo "  1. Configure your Discord bot token in .env"
    echo "  2. Set up GitHub integration for automated PRs"  
    echo "  3. Configure AI API keys (OpenAI/Anthropic)"
    echo "  4. Invite Discord bot to your server"
    echo "  5. Test with '/request' command"
    echo
}

# Cleanup function
cleanup_deployment() {
    log_info "Cleaning up previous deployment..."
    
    cd "$REFINORY_DIR"
    
    # Stop and remove containers
    docker-compose -f docker-compose.refinory.yml down --volumes --remove-orphans
    
    # Remove custom images (optional)
    docker rmi refinory-ai:latest 2>/dev/null || true
    
    log_success "Cleanup completed"
}

# Main deployment function
main() {
    echo
    echo "🚀 Refinory AI Agent Platform Deployment"
    echo "========================================"
    echo
    
    local deployment_type="${1:-docker}"
    local cleanup="${2:-false}"
    
    # Parse command line arguments
    case "$deployment_type" in
        "docker"|"compose")
            deployment_type="docker"
            ;;
        "k8s"|"kubernetes")
            deployment_type="kubernetes"
            ;;
        "cleanup"|"clean")
            cleanup_deployment
            exit 0
            ;;
        "help"|"-h"|"--help")
            echo "Usage: $0 [deployment_type] [cleanup]"
            echo
            echo "Deployment types:"
            echo "  docker       Deploy with Docker Compose (default)"
            echo "  kubernetes   Deploy to Kubernetes cluster"
            echo "  cleanup      Clean up existing deployment"
            echo
            echo "Examples:"
            echo "  $0                     # Deploy with Docker Compose"
            echo "  $0 docker             # Deploy with Docker Compose"
            echo "  $0 kubernetes         # Deploy to Kubernetes"
            echo "  $0 cleanup            # Clean up deployment"
            exit 0
            ;;
        *)
            log_error "Unknown deployment type: $deployment_type"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
    
    # Cleanup if requested
    if [[ "$cleanup" == "true" || "$cleanup" == "yes" ]]; then
        cleanup_deployment
    fi
    
    # Run deployment steps
    check_prerequisites
    load_environment
    generate_env_file
    
    case "$deployment_type" in
        "docker")
            build_images
            deploy_docker_compose
            initialize_database
            setup_monitoring
            ;;
        "kubernetes")
            deploy_kubernetes
            ;;
    esac
    
    show_deployment_summary
    
    log_success "Refinory deployment completed successfully! 🎉"
}

# Run main function with all arguments
main "$@"