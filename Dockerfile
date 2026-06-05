FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Make main.py executable
RUN chmod +x /app/src/main.py /app/src/netcat_proxy.py

# Set environment variable for graph config
ENV GRAPH_CONFIG=/app/src/methodology_graph.json

# Default command runs CTF Brain CLI
CMD ["python", "/app/src/main.py"]
