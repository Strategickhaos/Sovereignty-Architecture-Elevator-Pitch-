# SAGCO OS - Multi-stage Dockerfile
# Stages: base, dev, api

# ============ BASE STAGE ============
FROM python:3.11-slim as base

LABEL maintainer="Strategickhaos <info@strategickhaos.com>"
LABEL description="SAGCO - Sovereignty Architecture Governance Cognitive OS"
LABEL version="0.1.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash sagco

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml ./
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e ".[test]"

# Copy application code
COPY --chown=sagco:sagco . .

# Switch to non-root user
USER sagco

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.core import SAGCOKernel; print('OK')" || exit 1

CMD ["python", "-m", "src.core.sagco"]


# ============ DEV STAGE ============
FROM base as dev

USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    make \
    gcc \
    g++ \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install dev dependencies
RUN pip install -e ".[dev]"

# Install pre-commit hooks
RUN git init && pre-commit install || true

USER sagco

# Expose debug port
EXPOSE 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "src.core.sagco"]


# ============ API STAGE ============
FROM base as api

USER root

# Install additional API dependencies
RUN pip install \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    gunicorn>=21.2.0

USER sagco

# Expose API port
EXPOSE 8000

# Health check for API
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "src.api:app"]
