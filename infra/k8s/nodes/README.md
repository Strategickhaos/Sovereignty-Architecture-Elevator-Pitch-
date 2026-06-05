# K8s Node Personalities - Infrastructure with Character

## Purpose
Generate K8s manifests where nodes have distinct personalities through labels and taints, which the scheduler naturally respects.

## Node Personalities

### Nova - The Compute Powerhouse
```yaml
apiVersion: v1
kind: Node
metadata:
  name: nova-01
  labels:
    personality: nova
    role: compute-heavy
    hardware: rtx-4090
    specialty: ai-inference
  annotations:
    description: "High-performance compute node for AI workloads"
spec:
  taints:
    - key: workload-type
      value: compute-intensive
      effect: PreferNoSchedule
  capacity:
    cpu: "32"
    memory: "128Gi"
    nvidia.com/gpu: "2"
```

**Nova's Character**:
- Loves heavy lifting (matrix multiplications, LLM inference)
- Impatient with I/O-bound tasks
- Works best at night (cooler temperatures)

### Lyra - The Memory Maven
```yaml
apiVersion: v1
kind: Node
metadata:
  name: lyra-01
  labels:
    personality: lyra
    role: memory-heavy
    hardware: high-memory
    specialty: vector-database
  annotations:
    description: "High-memory node for vector databases and caching"
spec:
  taints:
    - key: workload-type
      value: memory-intensive
      effect: PreferNoSchedule
  capacity:
    cpu: "16"
    memory: "512Gi"
```

**Lyra's Character**:
- Remembers everything (Redis, pgvector, embeddings)
- Patient with large datasets
- Thrives on random access patterns

### Athena - The Balanced Operator
```yaml
apiVersion: v1
kind: Node
metadata:
  name: athena-01
  labels:
    personality: athena
    role: balanced
    hardware: standard
    specialty: general-purpose
  annotations:
    description: "Balanced node for general workloads"
spec:
  capacity:
    cpu: "16"
    memory: "64Gi"
```

**Athena's Character**:
- Jack of all trades
- Diplomatic (handles any workload)
- Reliable and steady

## Manifest Generator

```python
#!/usr/bin/env python3
"""
Generate K8s manifests with node personalities
"""

class NodePersonality:
    def __init__(self, name, role, specialty, resources, character):
        self.name = name
        self.role = role
        self.specialty = specialty
        self.resources = resources
        self.character = character
    
    def generate_manifest(self, instance_number):
        return f"""
apiVersion: v1
kind: Node
metadata:
  name: {self.name}-{instance_number:02d}
  labels:
    personality: {self.name}
    role: {self.role}
    specialty: {self.specialty}
    instance: "{instance_number}"
  annotations:
    character: "{self.character}"
spec:
  capacity:
    cpu: "{self.resources['cpu']}"
    memory: "{self.resources['memory']}"
"""

# Define personalities
PERSONALITIES = {
    'nova': NodePersonality(
        name='nova',
        role='compute-heavy',
        specialty='ai-inference',
        resources={'cpu': 32, 'memory': '128Gi'},
        character='Loves AI workloads, impatient with I/O'
    ),
    'lyra': NodePersonality(
        name='lyra',
        role='memory-heavy',
        specialty='vector-database',
        resources={'cpu': 16, 'memory': '512Gi'},
        character='Remembers everything, patient with data'
    ),
    'athena': NodePersonality(
        name='athena',
        role='balanced',
        specialty='general-purpose',
        resources={'cpu': 16, 'memory': '64Gi'},
        character='Balanced and reliable, handles anything'
    )
}

# Generate fleet
def generate_fleet():
    """Generate complete node fleet with personalities"""
    manifests = []
    
    # 3 Nova nodes (compute cluster)
    for i in range(1, 4):
        manifests.append(PERSONALITIES['nova'].generate_manifest(i))
    
    # 2 Lyra nodes (memory cluster)
    for i in range(1, 3):
        manifests.append(PERSONALITIES['lyra'].generate_manifest(i))
    
    # 5 Athena nodes (general cluster)
    for i in range(1, 6):
        manifests.append(PERSONALITIES['athena'].generate_manifest(i))
    
    return manifests

if __name__ == '__main__':
    fleet = generate_fleet()
    for manifest in fleet:
        print(manifest)
        print("---")
```

## Scheduler Affinity

Pods express preferences for node personalities:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: llm-inference
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            matchExpressions:
              - key: personality
                operator: In
                values:
                  - nova  # Prefers Nova for compute
  containers:
    - name: llm
      image: qwen2.5:72b
      resources:
        requests:
          nvidia.com/gpu: 1
```

## Personality-Aware Scheduler

```python
def schedule_pod(pod, nodes):
    """
    Personality-aware scheduling algorithm
    """
    # Analyze pod workload type
    workload_type = analyze_workload(pod)
    
    # Score nodes based on personality match
    scores = {}
    for node in nodes:
        personality = node.labels['personality']
        
        if workload_type == 'compute' and personality == 'nova':
            scores[node] = 100
        elif workload_type == 'memory' and personality == 'lyra':
            scores[node] = 100
        elif workload_type == 'balanced' and personality == 'athena':
            scores[node] = 100
        else:
            scores[node] = 50  # Can run, but not ideal
        
        # Adjust for current load
        scores[node] *= (1 - node.current_utilization())
    
    # Select best node
    best_node = max(scores.items(), key=lambda x: x[1])[0]
    return best_node
```

## Benefits

1. **Natural Affinity**: Scheduler respects node personalities
2. **Resource Optimization**: Right workload on right hardware
3. **Human-Readable**: Operators understand "Nova is for AI"
4. **Emergent Behavior**: Cluster self-organizes around strengths

This creates infrastructure with **character and purpose**, not just interchangeable resources.
