FROM python:3.11-slim

LABEL maintainer="Department of Living Memory <dolm@strategickhaos.com>"
LABEL description="DoLM Daemon - Department of Living Memory for tracking errors and TODOs"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy daemon code
COPY dolm_daemon.py .

# Create volumes for swarm and vault
VOLUME ["/swarm", "/vault"]

# Environment variables
ENV DOLM_WATCH_PATH=/swarm
ENV DOLM_VAULT_PATH=/vault
ENV PYTHONUNBUFFERED=1

# Run daemon
CMD ["python", "-u", "dolm_daemon.py"]
