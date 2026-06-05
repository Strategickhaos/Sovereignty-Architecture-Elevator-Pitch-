# Drift Detection - Infrastructure Monitoring

## Purpose
Detect when production drifts from declarative IaC using Meroitic Script test.

## Drift Detection

Compare production state to IaC:
- If difference > 0.1: Alert
- If difference > 0.3: Auto-correct
- If difference > 0.5: Emergency (manual intervention)

Prevents configuration drift.
