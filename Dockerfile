FROM python:3.11-slim

LABEL maintainer="Strategickhaos DAO LLC"
LABEL description="CTF Brain - Distributed Cognitive Orchestration Engine"

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ctf-brain/ /app/

# Make scripts executable
RUN chmod +x /app/main.py /app/netcat_proxy.py

# Default command (can be overridden)
CMD ["python", "/app/main.py"]
