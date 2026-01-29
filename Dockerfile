# TRIG6 Container - Zero Network Dependencies
FROM python:3.11-slim

LABEL org.opencontainers.image.title="TRIG6"
LABEL org.opencontainers.image.description="Deterministic Mathematical Engineering System"
LABEL org.opencontainers.image.authors="Domenic G. Garza"
LABEL org.opencontainers.image.vendor="Strategickhaos DAO LLC"

# Set working directory
WORKDIR /app

# Copy application files
COPY trig6.py /app/
COPY core/ /app/core/
COPY domains/ /app/domains/
COPY sagco/ /app/sagco/

# Make executable
RUN chmod +x /app/trig6.py && \
    chmod +x /app/sagco/bootloader.py

# No external dependencies - pure Python standard library
# Verify offline operation capability
RUN python3 -c "import sys, math; print('Python', sys.version)"

# Default entrypoint
ENTRYPOINT ["python3", "/app/trig6.py"]
CMD ["doctor"]
