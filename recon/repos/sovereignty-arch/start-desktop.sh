#!/bin/bash
# start-desktop.sh - CloudOS Desktop Launch Script
# Strategic Khaos Cloud Operating System

set -euo pipefail

COMPOSE_FILE="docker-compose-cloudos.yml"
PROJECT_NAME="cloudos"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

# Check dependencies
check_dependencies() {
    log "🔍 Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        error "Docker Compose is not available. Please update Docker."
        exit 1
    fi
    
    success "Dependencies verified"
}

# Create required directories
create_directories() {
    log "📁 Creating required directories..."
    
    mkdir -p {monitoring/{grafana/{provisioning/{dashboards,datasources},dashboards}},ssl,data/{postgres,redis,grafana,prometheus,qdrant,minio,keycloak,synapse}}
    mkdir -p /var/refinory/{artifacts,outputs}
    
    success "Directories created"
}

# Generate initial database script
create_db_init() {
    log "🗄️ Creating database initialization script..."
    
    cat > init-cloudos-db.sql << 'EOF'
-- CloudOS Database Initialization
CREATE DATABASE IF NOT EXISTS keycloak;
CREATE DATABASE IF NOT EXISTS synapse;
CREATE DATABASE IF NOT EXISTS strategickhaos;

-- Create users for services
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'keycloak') THEN
        CREATE USER keycloak WITH PASSWORD 'keycloak_password';
        GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
    END IF;
    
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'synapse') THEN
        CREATE USER synapse WITH PASSWORD 'synapse_password';
        GRANT ALL PRIVILEGES ON DATABASE synapse TO synapse;
    END IF;
END
$$;

-- Strategic Khaos schema
\c strategickhaos;

CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS refinory;
CREATE SCHEMA IF NOT EXISTS contradictions;

-- Basic tables for AI system
CREATE TABLE IF NOT EXISTS public.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS refinory.experts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contradictions.revenue_streams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hook TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    pricing TEXT NOT NULL,
    proof TEXT,
    demo_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial contradiction data
INSERT INTO contradictions.revenue_streams (name, hook, mechanism, pricing, proof, demo_url) VALUES
('Privacy vs Personalization', 'Tailored for you — never tracked.', 'On-device embeddings + zero-knowledge sync', '$0 logs → $9/mo for cross-device sync (E2EE)', 'curl /metrics | grep logs=0', 'https://demo.strategickhaos.com/privacy'),
('Speed vs Security', 'Login in 1.2s — or we pay you.', 'WebAuthn + risk engine (IP velocity, device fingerprint)', '$0.01 per failed step-up (SLO: 99.9% <2s)', 'Grafana: login_latency_p99', 'https://demo.strategickhaos.com/speed'),
('Simple vs Powerful', 'One click. Infinite possibilities.', 'Progressive disclosure + AI intent prediction', 'Free basics → $19/mo for power features', 'Feature usage analytics dashboard', 'https://demo.strategickhaos.com/progressive')
ON CONFLICT DO NOTHING;
EOF
    
    success "Database initialization script created"
}

# Set system limits
set_limits() {
    log "⚙️ Setting system limits..."
    
    # Increase file descriptor limits for containers
    ulimit -n 65535 2>/dev/null || warn "Could not set ulimit -n 65535 (requires sudo)"
    
    # Set Docker daemon limits if accessible
    if [ -w /etc/docker/daemon.json ]; then
        log "Setting Docker daemon limits..."
        cat > /etc/docker/daemon.json << 'EOF'
{
  "default-ulimits": {
    "nofile": {
      "Hard": 65535,
      "Name": "nofile",
      "Soft": 65535
    }
  }
}
EOF
        systemctl reload docker 2>/dev/null || warn "Could not reload Docker daemon"
    fi
    
    success "System limits configured"
}

# Start services
start_services() {
    log "🚀 Starting CloudOS services..."
    
    # Stop any existing services first
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down 2>/dev/null || true
    
    # Pull latest images
    log "📥 Pulling container images..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" pull
    
    # Build custom services
    log "🔨 Building custom services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" build --no-cache
    
    # Start infrastructure services first
    log "🏗️ Starting infrastructure services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d postgres redis qdrant
    
    # Wait for infrastructure to be ready
    sleep 10
    
    # Start application services
    log "🎯 Starting application services..."
    docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d
    
    success "All services starting..."
}

# Wait for services to be healthy
wait_for_services() {
    log "⏳ Waiting for services to become healthy..."
    
    local max_attempts=60
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        local healthy_count=0
        local total_services=0
        
        # Check each service
        while IFS= read -r service; do
            if [ -n "$service" ]; then
                total_services=$((total_services + 1))
                if docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps --format json | jq -r '.[] | select(.Name == "'$service'") | .Health' | grep -q "healthy\|running"; then
                    healthy_count=$((healthy_count + 1))
                fi
            fi
        done < <(docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps --services)
        
        if [ $healthy_count -eq $total_services ]; then
            success "All services are healthy!"
            break
        fi
        
        log "Services ready: $healthy_count/$total_services (attempt $((attempt + 1))/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -eq $max_attempts ]; then
        warn "Some services may still be starting. Continuing..."
    fi
}

# Verify endpoints
verify_endpoints() {
    log "🔍 Verifying endpoints..."
    
    local endpoints=(
        "IDE:http://localhost:8081"
        "Terminal:http://localhost:7681" 
        "AI SME:http://localhost:8000/health"
        "Chat:http://localhost:8009"
        "Keycloak:http://localhost:8180"
        "MinIO Console:http://localhost:9001"
        "Traefik Dashboard:http://localhost:8080"
        "Grafana:http://localhost:3000"
        "Prometheus:http://localhost:9090"
    )
    
    for endpoint in "${endpoints[@]}"; do
        local name="${endpoint%%:*}"
        local url="${endpoint##*:}"
        
        if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302\|401"; then
            success "✓ $name: $url"
        else
            warn "⚠ $name: $url (may still be starting)"
        fi
    done
}

# Display final status
show_status() {
    log "📊 CloudOS Status Dashboard"
    echo ""
    echo "🌐 Web Interfaces:"
    echo "  IDE (VS Code):      http://localhost:8081"
    echo "  Terminal (Wetty):   http://localhost:7681"  
    echo "  AI SME API:         http://localhost:8000"
    echo "  Chat (Element):     http://localhost:8009"
    echo "  Auth (Keycloak):    http://localhost:8180"
    echo "  Storage (MinIO):    http://localhost:9001"
    echo ""
    echo "🔧 Admin Interfaces:"
    echo "  Traefik Dashboard:  http://localhost:8080"
    echo "  Grafana:           http://localhost:3000"
    echo "  Prometheus:        http://localhost:9090"
    echo ""
    echo "🔑 Default Credentials:"
    echo "  IDE:               Password: admin"
    echo "  Keycloak:          admin / admin"
    echo "  MinIO:             admin / admin123"
    echo "  Grafana:           admin / admin"
    echo ""
    echo "🚀 CloudOS is ready for Strategic Khaos operations!"
}

# Main execution
main() {
    log "🎯 Strategic Khaos CloudOS Startup"
    echo ""
    
    check_dependencies
    create_directories
    create_db_init
    set_limits
    start_services
    wait_for_services
    verify_endpoints
    show_status
    
    success "🎉 CloudOS Desktop Environment Ready!"
}

# Run main function
main "$@"