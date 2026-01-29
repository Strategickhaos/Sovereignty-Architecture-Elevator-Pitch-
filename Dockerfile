# ============================================================
# TRIG6 SOVEREIGN COMPUTE ENGINE
# ============================================================
# 
# "It boots or it doesn't."
#
# Zero external dependencies. Deterministic math. Cited constants.
#
# Build:
#   docker build -t strategickhaos/trig6:latest .
#
# Run:
#   docker run --rm strategickhaos/trig6 doctor
#   docker run --rm strategickhaos/trig6 bridle --load 300 --theta 120
#   docker run --rm strategickhaos/trig6 cite rope.knot.figure_8_on_bight
#
# Owner: Strategickhaos DAO LLC
# Author: Domenic G. Garza
# License: MIT
# ============================================================

FROM python:3.11-slim AS base

LABEL org.opencontainers.image.title="TRIG6 Sovereign Compute Engine"
LABEL org.opencontainers.image.description="Physics compiler with regulatory citations"
LABEL org.opencontainers.image.vendor="Strategickhaos DAO LLC"
LABEL org.opencontainers.image.authors="Domenic G. Garza"
LABEL org.opencontainers.image.source="https://github.com/Strategickhaos/trig6"
LABEL org.opencontainers.image.licenses="MIT"

RUN groupadd -r trig6 && useradd -r -g trig6 trig6

WORKDIR /app

COPY trig6.py ./
COPY core/ ./core/
COPY domains/ ./domains/
COPY packs/ ./packs/
COPY games/ ./games/
COPY sagco/ ./sagco/

RUN mkdir -p /home/trig6/.khaos && \
    mkdir -p /home/trig6/.sagco && \
    chown -R trig6:trig6 /app /home/trig6

USER trig6
ENV HOME=/home/trig6

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 /app/trig6.py doctor | grep -q "PASS" || exit 1

ENTRYPOINT ["python3", "/app/trig6.py"]
CMD ["doctor"]
