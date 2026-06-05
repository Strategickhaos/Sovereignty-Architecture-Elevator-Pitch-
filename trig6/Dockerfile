FROM python:3.11-slim

# Metadata
LABEL maintainer="Domenic G. Garza <strategickhaos@gmail.com>"
LABEL description="TRIG6 Sovereign Compute Engine"
LABEL version="1.0.0"

# Create non-root user
RUN useradd -m -u 1000 trig6

# Set working directory
WORKDIR /app

# Copy TRIG6 files
COPY --chown=trig6:trig6 . /app/

# Make executable
RUN chmod +x /app/trig6.py

# Switch to non-root user
USER trig6

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PATH="/app:${PATH}"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 /app/trig6.py doctor || exit 1

# Default command
ENTRYPOINT ["python3", "/app/trig6.py"]
CMD ["doctor"]
