# Monitoring Stack - Enhanced Log Ingestion & Self-Evolution

This directory contains monitoring configurations for the Strategickhaos Sovereignty Architecture's enhanced log ingestion and self-improving system.

## Directory Structure

```
monitoring/
├── alerts.yml                          # Prometheus alerting rules (enhanced with anomaly detection)
├── prometheus.yml                      # Prometheus scrape configuration
├── loki-config.yml                     # Loki log aggregation configuration
├── log-enrichment-config.yml           # Log parsing and enrichment rules
├── synapsebus-config.yml               # SynapseBus nervous system configuration
├── grafana/
│   └── enhanced-log-analytics-dashboard.json  # Grafana dashboard
└── README.md                           # This file
```

## Components Overview

### 1. Log Enrichment (`log-enrichment-config.yml`)

Configures how raw Kubernetes logs are parsed, enriched, and routed:

- **Metadata Enrichment**: Adds cluster ID, event type, namespace tags
- **Event Classification**: Categorizes logs (reconciliation, scheduling, health, cross-cluster)
- **Intelligent Sampling**: 
  - Critical events: 100% capture
  - Warnings: 50% sampling
  - Health checks: 10% sampling
  - Default: 25% sampling
- **Cost Controls**: $2/month budget with automatic alerts
- **Storage Tiers**: Hot (7d), Warm (30d), Cold archive (90d)

### 2. SynapseBus Configuration (`synapsebus-config.yml`)

Defines the nervous system that converts log events (Spikes) into automated actions (Reflexes):

- **Spike Sources**: HTTP endpoints, Prometheus webhooks, Kubernetes event watches
- **Reflex Actions**: Auto-scaling, scheduler tuning, node redistribution, Discord alerts
- **Neural Pathways**: Pattern learning and predictive reflexes
- **Field Engine Integration**: Physics-based stability modeling
- **DNA Synthesis Integration**: Configuration evolution and A/B testing

### 3. Prometheus Configuration (`prometheus.yml`)

Scrape configs for all components:

- Discord bot and event gateway
- Refinory AI platform
- **New**: SynapseBus (port 9090)
- **New**: Field Engine (port 9091)
- **New**: DNA Synthesis Orchestrator (port 9092)
- **New**: Log Enrichment processors

### 4. Enhanced Alerts (`alerts.yml`)

Six categories of alerts:

1. **Discord & Webhook Alerts**: Bot health, rate limits, processing latency
2. **Refinory AI Alerts**: API health, task failures, request backlog
3. **Infrastructure Alerts**: Redis, PostgreSQL, Vault, Qdrant health
4. **System Alerts**: Memory, disk, container restarts
5. **Anomaly Detection Alerts** (NEW):
   - API call spikes (>2x baseline)
   - Slow reconciliation loops (>5s)
   - Cross-cluster event correlation
   - Pod scheduling latency anomalies
   - Predictive CPU saturation
   - Network traffic spikes
   - Log volume anomalies
   - Cross-node behavior patterns
6. **SynapseBus & Evolution Alerts** (NEW):
   - SynapseBus health
   - Reflex failure rates
   - Neural pattern detection
   - Field stability warnings
   - DNA synthesis completion
7. **Cost & Efficiency Alerts** (NEW):
   - Budget approach warnings
   - Logs-per-dollar ratio degradation
   - Sampling rate optimization needed

### 5. Grafana Dashboard

Comprehensive visualization with panels for:

- **Log Processing**: Processed vs sampled rates, cost metrics, logs-per-dollar ratio
- **Anomaly Detection**: Active anomalies timeline
- **SynapseBus Activity**: Spikes, reflexes, success rates, neural patterns
- **Field Engine**: Stability score, vector count, magnitude tracking
- **DNA Synthesis**: Evolution runs, A/B tests, configuration variants
- **Cross-Cluster**: Event correlation by cluster
- **System Health**: Component status table

## Quick Start

### 1. Deploy Monitoring Stack

```bash
# Apply Prometheus and Loki configs
kubectl apply -f prometheus.yml
kubectl apply -f loki-config.yml
kubectl apply -f alerts.yml

# Deploy enhanced components
cd ..
./scripts/deploy-enhanced-logging.sh
```

### 2. Import Grafana Dashboard

1. Access Grafana (usually at http://grafana.monitoring.svc.cluster.local)
2. Navigate to: Dashboards → Import
3. Upload: `grafana/enhanced-log-analytics-dashboard.json`
4. Select Prometheus data source
5. Click "Import"

### 3. Verify Metrics

```bash
# Check Prometheus targets
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Visit http://localhost:9090/targets

# Expected targets:
# - synapsebus:9090 (UP)
# - field-engine:9091 (UP)
# - dna-synthesis-orchestrator:9092 (UP)
# - log-enrichment:9090 (UP)
```

## Configuration

### Adjust Sampling Rates

Edit `log-enrichment-config.yml`:

```yaml
sampling:
  rules:
    - name: "critical-events"
      sample_rate: 1.0  # 100% of critical events
    - name: "warnings"
      sample_rate: 0.5  # 50% of warnings
    - name: "health-checks"
      sample_rate: 0.1  # 10% of health checks
    - name: "default"
      sample_rate: 0.25  # 25% default
```

Then reload the configuration:
```bash
kubectl rollout restart daemonset/log-enrichment -n kube-system
```

### Tune Reflex Thresholds

Edit `synapsebus-config.yml`:

```yaml
reflexes:
  - name: "scale-on-slow-reconciliation"
    trigger:
      threshold:
        duration_ms: 5000  # Adjust threshold
        frequency: "3 events in 5m"
```

Then reload:
```bash
kubectl rollout restart deployment/synapsebus -n kube-system
```

### Modify Cost Budget

Edit `log-enrichment-config.yml`:

```yaml
cost_controls:
  monthly_budget_usd: 2.0  # Increase if needed
  budget_alerts:
    - threshold: 0.8  # Alert at 80%
    - threshold: 0.95  # Critical at 95%
```

## Monitoring Best Practices

### 1. Watch Key Metrics

```bash
# SynapseBus health
watch -n 5 'kubectl exec -n kube-system deploy/synapsebus -- \
  curl -s http://localhost:8080/health'

# Field stability
watch -n 10 'kubectl exec -n kube-system deploy/field-engine -- \
  curl -s http://localhost:8081/api/v1/field/status'

# Cost tracking
watch -n 300 'kubectl exec -n kube-system deploy/synapsebus -- \
  curl -s http://localhost:9090/metrics | grep estimated_monthly_cost'
```

### 2. Review Anomalies Daily

In Grafana dashboard:
- Check "Active Anomalies" panel
- Review "Reflex Success Rate" (should be >90%)
- Monitor "Field Stability Score" (should be >0.6)
- Track "Logs per Dollar" ratio (target: >36M logs/$1)

### 3. Evaluate Evolution Weekly

```bash
# Check DNA synthesis activity
kubectl logs -n kube-system deploy/dna-synthesis-orchestrator --tail=100 | grep "synthesis"

# List A/B tests
kubectl exec -n kube-system deploy/dna-synthesis-orchestrator -- \
  curl -s http://localhost:8082/api/v1/ab-tests
```

## Troubleshooting

### High Alert Volume

If getting too many anomaly alerts:

1. **Adjust baselines** in `alerts.yml`:
   ```yaml
   # Change from >2x to >3x baseline
   expr: (rate(...) / avg_over_time(...)) > 3
   ```

2. **Increase alert duration**:
   ```yaml
   for: 5m  # Change to 10m or 15m
   ```

### Cost Overrun

If approaching budget:

1. **Increase sampling aggressiveness**:
   ```yaml
   sample_rate: 0.15  # Reduce from 0.25 to 0.15
   ```

2. **Reduce hot retention**:
   ```yaml
   hot_retention_days: 3  # Reduce from 7
   ```

3. **Add more exclusions**:
   ```yaml
   exclude_patterns:
     - ".*debug.*"
     - ".*trace.*"
   ```

### Reflex Failures

Check SynapseBus logs:
```bash
kubectl logs -n kube-system deploy/synapsebus --tail=200 | grep -i error
```

Common issues:
- **RBAC permissions**: Verify ServiceAccount has required permissions
- **Cooldown conflicts**: Check if cooldowns are too long
- **Target not found**: Verify deployment/configmap names are correct

### Field Instability

If stability score persistently low (<0.6):

1. **Identify problem areas**:
   ```bash
   # Check which namespaces have most events
   kubectl exec -n kube-system deploy/field-engine -- \
     curl -s http://localhost:8081/api/v1/field/status
   ```

2. **Review event clustering** in Grafana "Events by Cluster" panel

3. **Trigger manual redistribution** if needed

## Metrics Reference

### SynapseBus Metrics

- `spikes_received_total`: Total spikes received by type
- `spikes_processed_total`: Total spikes processed
- `reflexes_triggered_total`: Reflexes triggered by name
- `reflex_success_total`: Successful reflex executions
- `reflex_failure_total`: Failed reflex executions
- `neural_patterns_detected_total`: Patterns detected by name
- `spike_processing_duration_seconds`: Histogram of processing time

### Field Engine Metrics

- `field_stability_score`: Cluster stability (0-1, >0.6 is stable)
- `field_magnitude`: Total field magnitude
- `field_vector_count`: Active field vectors
- `field_instability_events_total`: Instability events detected

### DNA Synthesis Metrics

- `dna_synthesis_runs_total`: Total synthesis runs
- `dna_synthesis_success_total`: Successful syntheses
- `dna_synthesis_failure_total`: Failed syntheses
- `ab_tests_active`: Number of active A/B tests
- `evolution_score`: Configuration evolution quality score

### Log Enrichment Metrics

- `logs_processed_total`: Total logs processed
- `logs_sampled_total`: Logs kept after sampling
- `logs_enriched_total`: Logs successfully enriched
- `synapse_spikes_sent_total`: Spikes sent to SynapseBus
- `parse_errors_total`: Parse failures
- `log_processing_duration_seconds`: Histogram of processing time
- `estimated_monthly_cost_usd`: Current month-to-date cost estimate
- `hot_storage_bytes`: Hot storage usage
- `cold_storage_bytes`: Cold storage usage

## Security Notes

- All components run with least-privilege RBAC
- Logs are sampled to reduce PII exposure
- Discord webhook URLs stored as Kubernetes Secrets
- Inter-component communication uses ClusterIP services
- Consider enabling TLS for external endpoints

## Support

For issues or questions:
1. Check logs: `kubectl logs -n kube-system -l app=<component>`
2. Review metrics: `kubectl port-forward -n kube-system svc/<component> 9090:9090`
3. Consult main documentation: `../docs/ENHANCED_LOG_INGESTION.md`
4. Open issue in repository

---

**From 72M logs at $2/month to intelligent, self-evolving infrastructure** 🔥
