# Spot Strategy - Cost Optimization

## Purpose
Dynamic workload placement using spot market pricing and simulated annealing.

## Strategy

- Monitor spot prices across availability zones
- Move non-critical workloads to cheap zones
- Use simulated annealing to find optimal placement
- Target: 60-80% cost reduction on batch workloads

Market temperature = Average spot price
