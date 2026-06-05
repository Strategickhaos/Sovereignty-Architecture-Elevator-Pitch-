# Multi-stage Dockerfile for SAGCO OS
# Sovereignty Architecture Grand Central Operating System

# =============================================================================
# BASE STAGE - Common dependencies
# =============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 sagco && \
    mkdir -p /app /var/log/sagco && \
    chown -R sagco:sagco /app /var/log/sagco

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=sagco:sagco . .

# =============================================================================
# DEV STAGE - Development environment
# =============================================================================
FROM base as dev

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

# Switch to app user
USER sagco

# Expose ports
EXPOSE 8000 5678

# Development command
CMD ["python", "-m", "src.core.sagco", "config/sagco.yaml"]

# =============================================================================
# API STAGE - Production API server
# =============================================================================
FROM base as api

# Install production server
RUN pip install --no-cache-dir \
    gunicorn \
    uvicorn[standard]

# Copy only necessary files
COPY --chown=sagco:sagco src/ /app/src/
COPY --chown=sagco:sagco config/ /app/config/

# Switch to app user
USER sagco

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Production command
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# =============================================================================
# WORKER STAGE - Background task worker
# =============================================================================
FROM base as worker

# Copy application code
COPY --chown=sagco:sagco src/ /app/src/
COPY --chown=sagco:sagco config/ /app/config/

# Switch to app user
USER sagco

# Worker command
CMD ["python", "-m", "src.workers.task_worker"]
