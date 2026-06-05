# SAGCO OS - Makefile
# Version: 0.1.0

.PHONY: help dev test build deploy clean status logs k8s-apply k8s-status gke-deploy

# ===== Configuration =====
PROJECT_NAME := sagco-os
VERSION := 0.1.0
DOCKER_IMAGE := $(PROJECT_NAME):$(VERSION)
DOCKER_REGISTRY := gcr.io/PROJECT_ID
K8S_NAMESPACE := sagco
GKE_CLUSTER := sagco-cluster
GKE_REGION := us-central1

# ===== Help =====
help: ## Show this help message
	@echo "SAGCO OS v$(VERSION) - Makefile Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ===== Development =====
dev: ## Start local development environment (Docker Compose)
	@echo "Starting SAGCO development environment..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "  - SAGCO API: http://localhost:8000"
	@echo "  - Grafana: http://localhost:3000 (admin/sagco_admin)"
	@echo "  - Prometheus: http://localhost:9091"
	@make status

dev-build: ## Build and start development environment
	@echo "Building SAGCO development environment..."
	docker-compose build --no-cache
	docker-compose up -d
	@make status

stop: ## Stop development environment
	@echo "Stopping SAGCO development environment..."
	docker-compose down
	@echo "✓ Services stopped"

restart: ## Restart development environment
	@make stop
	@make dev

status: ## Check status of all services
	@echo "SAGCO Services Status:"
	@docker-compose ps

logs: ## Show logs from all services
	docker-compose logs -f

logs-sagco: ## Show SAGCO service logs only
	docker-compose logs -f sagco

shell: ## Open shell in SAGCO container
	docker-compose exec sagco /bin/bash

# ===== Testing =====
test: ## Run all tests
	@echo "Running SAGCO tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing

test-watch: ## Run tests in watch mode
	@echo "Running tests in watch mode..."
	ptw tests/ -- -v

test-coverage: ## Generate test coverage report
	@echo "Generating coverage report..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated in htmlcov/index.html"

lint: ## Run linting checks
	@echo "Running linting checks..."
	black --check src/ tests/
	flake8 src/ tests/
	mypy src/
	@echo "✓ Linting passed"

format: ## Format code with black and isort
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "✓ Code formatted"

# ===== Build =====
build: ## Build Docker image
	@echo "Building Docker image: $(DOCKER_IMAGE)"
	docker build -t $(DOCKER_IMAGE) .
	@echo "✓ Image built: $(DOCKER_IMAGE)"

build-dev: ## Build development Docker image
	@echo "Building development Docker image..."
	docker build --target dev -t $(DOCKER_IMAGE)-dev .
	@echo "✓ Dev image built"

build-api: ## Build API Docker image
	@echo "Building API Docker image..."
	docker build --target api -t $(DOCKER_IMAGE)-api .
	@echo "✓ API image built"

push: ## Push Docker image to registry
	@echo "Tagging and pushing to registry..."
	docker tag $(DOCKER_IMAGE) $(DOCKER_REGISTRY)/$(DOCKER_IMAGE)
	docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE)
	@echo "✓ Image pushed to $(DOCKER_REGISTRY)"

# ===== Production =====
prod-up: ## Start production stack (docker-compose.prod.yml)
	@echo "Starting SAGCO production stack..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✓ Production services started"

prod-down: ## Stop production stack
	@echo "Stopping production stack..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
	@echo "✓ Production services stopped"

prod-logs: ## Show production logs
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# ===== Kubernetes =====
k8s-apply: ## Deploy to Kubernetes
	@echo "Deploying SAGCO to Kubernetes..."
	kubectl create namespace $(K8S_NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -f k8s/sagco-deployment.yaml
	@echo "✓ Deployed to Kubernetes namespace: $(K8S_NAMESPACE)"

k8s-delete: ## Delete from Kubernetes
	@echo "Deleting SAGCO from Kubernetes..."
	kubectl delete -f k8s/sagco-deployment.yaml
	@echo "✓ Deleted from Kubernetes"

k8s-status: ## Check Kubernetes deployment status
	@echo "SAGCO Kubernetes Status:"
	@echo ""
	@echo "Namespace:"
	kubectl get namespace $(K8S_NAMESPACE)
	@echo ""
	@echo "Pods:"
	kubectl get pods -n $(K8S_NAMESPACE)
	@echo ""
	@echo "Services:"
	kubectl get services -n $(K8S_NAMESPACE)
	@echo ""
	@echo "Ingress:"
	kubectl get ingress -n $(K8S_NAMESPACE)
	@echo ""
	@echo "HPA:"
	kubectl get hpa -n $(K8S_NAMESPACE)

k8s-logs: ## Show Kubernetes logs
	kubectl logs -n $(K8S_NAMESPACE) -l app=sagco -f

k8s-describe: ## Describe Kubernetes deployment
	kubectl describe deployment sagco -n $(K8S_NAMESPACE)

k8s-shell: ## Open shell in Kubernetes pod
	kubectl exec -it -n $(K8S_NAMESPACE) $$(kubectl get pod -n $(K8S_NAMESPACE) -l app=sagco -o jsonpath='{.items[0].metadata.name}') -- /bin/bash

# ===== GKE =====
gke-create-cluster: ## Create GKE cluster
	@echo "Creating GKE cluster: $(GKE_CLUSTER)"
	gcloud container clusters create $(GKE_CLUSTER) \
		--region $(GKE_REGION) \
		--num-nodes 3 \
		--machine-type n1-standard-2 \
		--enable-autoscaling \
		--min-nodes 2 \
		--max-nodes 10 \
		--enable-autorepair \
		--enable-autoupgrade \
		--enable-stackdriver-kubernetes
	@echo "✓ GKE cluster created"

gke-get-credentials: ## Get GKE credentials
	@echo "Getting GKE credentials..."
	gcloud container clusters get-credentials $(GKE_CLUSTER) --region $(GKE_REGION)
	@echo "✓ Credentials configured"

gke-deploy: gke-get-credentials build push k8s-apply ## Deploy to GKE (full pipeline)
	@echo "Deploying GKE-specific resources..."
	kubectl apply -f k8s/gke/sagco-gke.yaml
	@echo "✓ Deployed to GKE"

gke-status: ## Check GKE deployment status
	@make k8s-status
	@echo ""
	@echo "GKE-specific resources:"
	kubectl get backendconfig -n $(K8S_NAMESPACE)
	kubectl get managedcertificate -n $(K8S_NAMESPACE)

gke-delete-cluster: ## Delete GKE cluster
	@echo "Deleting GKE cluster: $(GKE_CLUSTER)"
	gcloud container clusters delete $(GKE_CLUSTER) --region $(GKE_REGION) --quiet
	@echo "✓ GKE cluster deleted"

# ===== Helm =====
helm-install: ## Install with Helm
	@echo "Installing SAGCO with Helm..."
	helm install sagco ./helm/sagco -n $(K8S_NAMESPACE) --create-namespace
	@echo "✓ Installed with Helm"

helm-upgrade: ## Upgrade Helm release
	@echo "Upgrading SAGCO Helm release..."
	helm upgrade sagco ./helm/sagco -n $(K8S_NAMESPACE)
	@echo "✓ Helm release upgraded"

helm-uninstall: ## Uninstall Helm release
	@echo "Uninstalling SAGCO Helm release..."
	helm uninstall sagco -n $(K8S_NAMESPACE)
	@echo "✓ Helm release uninstalled"

helm-lint: ## Lint Helm chart
	helm lint ./helm/sagco

# ===== Database =====
db-shell: ## Connect to PostgreSQL shell
	docker-compose exec postgres psql -U sagco -d sagco

db-migrate: ## Run database migrations
	@echo "Running database migrations..."
	docker-compose exec sagco alembic upgrade head
	@echo "✓ Migrations complete"

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "⚠️  Resetting database..."
	docker-compose down -v
	docker-compose up -d postgres
	@echo "Waiting for postgres to be ready..."
	@sleep 5
	docker-compose up -d
	@echo "✓ Database reset complete"

# ===== Monitoring =====
metrics: ## View Prometheus metrics
	@echo "Opening Prometheus..."
	open http://localhost:9091

dashboards: ## View Grafana dashboards
	@echo "Opening Grafana..."
	@echo "Credentials: admin / sagco_admin"
	open http://localhost:3000

# ===== Utilities =====
clean: ## Clean up containers, images, and volumes
	@echo "Cleaning up..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "✓ Cleanup complete"

clean-all: ## Clean up everything including images
	@echo "Deep cleaning..."
	docker-compose down -v --rmi all --remove-orphans
	docker system prune -af --volumes
	@echo "✓ Deep cleanup complete"

install-deps: ## Install Python dependencies
	@echo "Installing dependencies..."
	pip install -e ".[dev]"
	@echo "✓ Dependencies installed"

init: install-deps ## Initialize project (install deps + setup)
	@echo "Initializing SAGCO project..."
	@make install-deps
	@echo "Setting up pre-commit hooks..."
	pre-commit install
	@echo "✓ Project initialized"

version: ## Show version information
	@echo "SAGCO OS v$(VERSION)"
	@echo "Docker Image: $(DOCKER_IMAGE)"
	@echo "Namespace: $(K8S_NAMESPACE)"

# ===== CI/CD =====
ci: lint test ## Run CI checks (lint + test)
	@echo "✓ CI checks passed"

cd: build push gke-deploy ## Run CD pipeline (build + push + deploy)
	@echo "✓ CD pipeline complete"

# ===== Default =====
.DEFAULT_GOAL := help
