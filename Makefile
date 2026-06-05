# SAGCO OS - Makefile
# Sovereignty Architecture Grand Central Operating System
# Automation commands for development, deployment, and operations

.PHONY: help dev test build deploy clean status logs

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_PROD := docker-compose -f docker-compose.yml -f docker-compose.prod.yml
KUBECTL := kubectl
PYTHON := python3
PROJECT_NAME := sagco
NAMESPACE := sagco

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Help

help: ## Display this help message
	@echo "$(CYAN)SAGCO OS v0.1.0 - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(CYAN)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(CYAN)%-15s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

dev: ## Start local development environment
	@echo "$(GREEN)Starting SAGCO development environment...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ SAGCO is running!$(NC)"
	@echo "  - API: http://localhost:8000"
	@echo "  - Grafana: http://localhost:3000 (admin/sagco_admin)"
	@echo "  - Prometheus: http://localhost:9090"

dev-build: ## Build and start development environment
	@echo "$(GREEN)Building and starting SAGCO...$(NC)"
	$(DOCKER_COMPOSE) up -d --build

stop: ## Stop development environment
	@echo "$(YELLOW)Stopping SAGCO...$(NC)"
	$(DOCKER_COMPOSE) down

restart: stop dev ## Restart development environment

clean: ## Clean up containers, volumes, and cache
	@echo "$(RED)Cleaning up SAGCO environment...$(NC)"
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

logs: ## Show logs from all services
	$(DOCKER_COMPOSE) logs -f

logs-sagco: ## Show SAGCO application logs
	$(DOCKER_COMPOSE) logs -f sagco

shell: ## Open shell in SAGCO container
	$(DOCKER_COMPOSE) exec sagco /bin/bash

##@ Testing

test: ## Run unit tests
	@echo "$(GREEN)Running SAGCO tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=src/core --cov-report=term-missing

test-quick: ## Run quick tests (no coverage)
	@echo "$(GREEN)Running quick tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v -x

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	$(PYTHON) -m pytest-watch tests/

lint: ## Run code linters
	@echo "$(GREEN)Linting code...$(NC)"
	$(PYTHON) -m black --check src/ tests/
	$(PYTHON) -m flake8 src/ tests/
	$(PYTHON) -m mypy src/

format: ## Format code
	@echo "$(GREEN)Formatting code...$(NC)"
	$(PYTHON) -m black src/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

##@ Building

build: ## Build Docker image
	@echo "$(GREEN)Building SAGCO Docker image...$(NC)"
	docker build -t $(PROJECT_NAME):latest -t $(PROJECT_NAME):0.1.0 .
	@echo "$(GREEN)✓ Build complete$(NC)"

build-prod: ## Build production Docker image
	@echo "$(GREEN)Building production SAGCO image...$(NC)"
	docker build --target api -t $(PROJECT_NAME):latest -t $(PROJECT_NAME):0.1.0 .
	@echo "$(GREEN)✓ Production build complete$(NC)"

##@ Kubernetes

k8s-apply: ## Deploy to Kubernetes
	@echo "$(GREEN)Deploying SAGCO to Kubernetes...$(NC)"
	$(KUBECTL) apply -f k8s/sagco-deployment.yaml
	@echo "$(GREEN)✓ Deployment applied$(NC)"

k8s-delete: ## Delete from Kubernetes
	@echo "$(RED)Deleting SAGCO from Kubernetes...$(NC)"
	$(KUBECTL) delete -f k8s/sagco-deployment.yaml

k8s-status: ## Check Kubernetes deployment status
	@echo "$(CYAN)SAGCO Kubernetes Status:$(NC)"
	@echo ""
	@echo "$(YELLOW)Namespace:$(NC)"
	$(KUBECTL) get namespace $(NAMESPACE) 2>/dev/null || echo "  Namespace not found"
	@echo ""
	@echo "$(YELLOW)Pods:$(NC)"
	$(KUBECTL) get pods -n $(NAMESPACE) 2>/dev/null || echo "  No pods found"
	@echo ""
	@echo "$(YELLOW)Services:$(NC)"
	$(KUBECTL) get services -n $(NAMESPACE) 2>/dev/null || echo "  No services found"
	@echo ""
	@echo "$(YELLOW)Ingress:$(NC)"
	$(KUBECTL) get ingress -n $(NAMESPACE) 2>/dev/null || echo "  No ingress found"

k8s-logs: ## Show Kubernetes pod logs
	@echo "$(CYAN)SAGCO Pod Logs:$(NC)"
	$(KUBECTL) logs -n $(NAMESPACE) -l app=$(PROJECT_NAME) --tail=100 -f

k8s-describe: ## Describe Kubernetes resources
	@echo "$(CYAN)SAGCO Deployment Description:$(NC)"
	$(KUBECTL) describe deployment $(PROJECT_NAME) -n $(NAMESPACE)

k8s-scale: ## Scale deployment (usage: make k8s-scale REPLICAS=5)
	@echo "$(GREEN)Scaling SAGCO to $(REPLICAS) replicas...$(NC)"
	$(KUBECTL) scale deployment/$(PROJECT_NAME) -n $(NAMESPACE) --replicas=$(REPLICAS)

##@ GKE (Google Kubernetes Engine)

gke-deploy: ## Deploy to GKE
	@echo "$(GREEN)Deploying SAGCO to GKE...$(NC)"
	$(KUBECTL) apply -f k8s/sagco-deployment.yaml
	$(KUBECTL) apply -f k8s/gke/sagco-gke.yaml
	@echo "$(GREEN)✓ GKE deployment complete$(NC)"

gke-status: ## Check GKE deployment status
	@echo "$(CYAN)SAGCO GKE Status:$(NC)"
	@$(MAKE) k8s-status
	@echo ""
	@echo "$(YELLOW)GKE-specific resources:$(NC)"
	$(KUBECTL) get managedcertificate -n $(NAMESPACE) 2>/dev/null || echo "  No managed certificates found"
	$(KUBECTL) get backendconfig -n $(NAMESPACE) 2>/dev/null || echo "  No backend configs found"

gke-ip: ## Get GKE external IP
	@echo "$(CYAN)SAGCO External IP:$(NC)"
	$(KUBECTL) get ingress sagco-gke -n $(NAMESPACE) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
	@echo ""

##@ Database

db-migrate: ## Run database migrations
	@echo "$(GREEN)Running database migrations...$(NC)"
	$(DOCKER_COMPOSE) exec sagco python -m alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

db-shell: ## Open PostgreSQL shell
	@echo "$(CYAN)Opening PostgreSQL shell...$(NC)"
	$(DOCKER_COMPOSE) exec postgres psql -U sagco -d sagco

db-backup: ## Backup database
	@echo "$(GREEN)Backing up database...$(NC)"
	$(DOCKER_COMPOSE) exec postgres pg_dump -U sagco sagco > backup-$(shell date +%Y%m%d-%H%M%S).sql
	@echo "$(GREEN)✓ Backup complete$(NC)"

db-restore: ## Restore database (usage: make db-restore FILE=backup.sql)
	@echo "$(YELLOW)Restoring database from $(FILE)...$(NC)"
	cat $(FILE) | $(DOCKER_COMPOSE) exec -T postgres psql -U sagco -d sagco
	@echo "$(GREEN)✓ Restore complete$(NC)"

##@ Status & Monitoring

status: ## Show status of all services
	@echo "$(CYAN)SAGCO System Status:$(NC)"
	@echo ""
	$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(YELLOW)Health Checks:$(NC)"
	@curl -s http://localhost:8000/health 2>/dev/null || echo "  API: $(RED)DOWN$(NC)"
	@curl -s http://localhost:9090/-/healthy 2>/dev/null && echo "  Prometheus: $(GREEN)UP$(NC)" || echo "  Prometheus: $(RED)DOWN$(NC)"
	@curl -s http://localhost:3000/api/health 2>/dev/null && echo "  Grafana: $(GREEN)UP$(NC)" || echo "  Grafana: $(RED)DOWN$(NC)"

metrics: ## Show current metrics
	@echo "$(CYAN)SAGCO Metrics:$(NC)"
	@curl -s http://localhost:9090/api/v1/query?query=up | jq .

##@ Installation

install-deps: ## Install Python dependencies
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

setup: ## Setup development environment
	@echo "$(GREEN)Setting up SAGCO development environment...$(NC)"
	@$(MAKE) install-deps
	@$(MAKE) build
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make dev' to start the development environment"
	@echo "  2. Run 'make test' to run tests"
	@echo "  3. Visit http://localhost:8000 to access the API"

##@ CI/CD

ci-test: ## Run CI tests
	@echo "$(GREEN)Running CI test suite...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=src/core --cov-report=xml --cov-report=term

ci-build: ## Build for CI
	@echo "$(GREEN)Building for CI...$(NC)"
	docker build --target api -t $(PROJECT_NAME):ci .

ci-lint: ## Run all linters for CI
	@echo "$(GREEN)Running CI linters...$(NC)"
	$(PYTHON) -m black --check src/ tests/
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=100
	$(PYTHON) -m mypy src/

##@ Documentation

docs: ## Generate documentation
	@echo "$(GREEN)Generating documentation...$(NC)"
	@echo "Documentation location: docs/"
	@echo "Run 'make docs-serve' to view locally"

docs-serve: ## Serve documentation locally
	@echo "$(GREEN)Serving documentation at http://localhost:8080$(NC)"
	python -m http.server 8080 -d docs/

##@ Utilities

version: ## Show version information
	@echo "$(CYAN)SAGCO OS Version Information:$(NC)"
	@echo "  Version: 0.1.0"
	@echo "  Python: $(shell python --version)"
	@echo "  Docker: $(shell docker --version)"
	@echo "  Kubernetes: $(shell kubectl version --client --short 2>/dev/null || echo 'Not installed')"

env: ## Show environment information
	@echo "$(CYAN)Environment Information:$(NC)"
	@echo "  Project: $(PROJECT_NAME)"
	@echo "  Namespace: $(NAMESPACE)"
	@echo "  Docker Compose: $(shell which docker-compose)"
	@echo "  Kubectl: $(shell which kubectl || echo 'Not found')"

watch: ## Watch service status
	@echo "$(CYAN)Watching SAGCO status (Ctrl+C to stop)...$(NC)"
	@watch -n 2 "docker-compose ps && echo '\n\n=== Health Status ===' && curl -s http://localhost:8000/health 2>/dev/null || echo 'API: DOWN'"
