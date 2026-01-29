FROM python:3.11-slim

LABEL org.opencontainers.image.title="TRIG6 Sovereign Compute Engine"
LABEL org.opencontainers.image.source="https://github.com/Strategickhaos/trig6"
LABEL org.opencontainers.image.licenses="MIT"

RUN groupadd -r trig6 && useradd -r -g trig6 trig6

WORKDIR /app

COPY trig6.py ./trig6.py
COPY proof.py ./proof.py
COPY core/ ./core/
COPY domains/ ./domains/
COPY packs/ ./packs/
COPY games/ ./games/
COPY sagco/ ./sagco/

RUN mkdir -p /home/trig6/.khaos /home/trig6/.sagco && \
    chown -R trig6:trig6 /app /home/trig6

USER trig6
ENV HOME=/home/trig6

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 /app/trig6.py doctor | grep -q "PASS" || exit 1

ENTRYPOINT ["python3", "/app/trig6.py"]
CMD ["doctor"]
