FROM python:3.11-slim

LABEL maintainer="Strategickhaos DAO LLC"
LABEL invention="INV-078"
LABEL version="1.0.0"
LABEL description="FlameLang Physics Compiler - Semantic Physics Compilation"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY hebrew_operators.py .
COPY cmb_anomaly_detector.py .
COPY flamelang_physics_compiler.py .

# Create data directory for Planck data
RUN mkdir -p /data/planck_2018

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLAMELANG_MODE=production
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import hebrew_operators; print('healthy')" || exit 1

# Default command runs the compiler demo
CMD ["python3", "flamelang_physics_compiler.py"]
