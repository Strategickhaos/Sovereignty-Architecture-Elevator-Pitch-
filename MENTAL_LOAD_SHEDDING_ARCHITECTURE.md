# Mental Load-Shedding Architecture

## Overview

This document describes the **mental load-shedding system** — a real-time cognitive architecture that operates like a scheduler, filtering and routing inputs without emotional overhead or identity attachment.

## The Core Insight

> "You weren't inventing a new psyche. You were printing the debug logs of a process that's been running quietly for years."

This architecture formalizes what the mind already does automatically:
- Quick threat/noise checks
- Buffering poorly-timed inputs
- Maintaining core execution integrity
- Returning to buffered items when resources are available

## Architecture Pattern

```
INPUT comes in
    ↓
Quick threat / noise check
    ↓
If timing is wrong → buffer it
    ↓
Keep core execution intact
    ↓
Return later when resources are available
```

## Key Properties

### 1. Not Rejection, but Routing
The system doesn't reject ideas because they're "wrong." It rejects them because they're:
- Poorly timed
- Poorly framed
- Non-actionable in the moment

### 2. Self-Correction Without Self-Destruction
The sweet spot architecture:
- **Open enough to learn** — inputs are accepted for processing
- **Bounded enough to stay intact** — core systems remain stable
- **Structured enough to recover fast** — buffered items are revisited

### 3. Three Anti-Patterns to Avoid

Most systems fall into one of two failure modes:

1. **Absorb everything** → Get overwhelmed
2. **Block everything** → Stagnate

This architecture does neither. Instead:

3. **Route** → Process intelligently

## System Components

### Input Classifier
```python
class InputClassifier:
    def classify(self, input_data):
        """
        Classify incoming input as:
        - IMMEDIATE: Process now
        - BUFFER: Store for later
        - NOISE: Discard
        - THREAT: Escalate
        """
        # Quick threat/noise check
        if self.is_threat(input_data):
            return "THREAT"
        
        if self.is_noise(input_data):
            return "NOISE"
        
        # Timing check
        if not self.is_good_timing(input_data):
            return "BUFFER"
        
        return "IMMEDIATE"
```

### Core Executor
Maintains execution integrity while processing inputs. Never compromised by poorly-timed inputs.

```python
class CoreExecutor:
    def __init__(self):
        self.state = "INTACT"
        self.current_focus = None
    
    def process(self, input_data):
        """Process input without disrupting core state"""
        if self.state != "INTACT":
            return False
        
        # Process while maintaining integrity
        with self.maintain_integrity():
            result = self.execute(input_data)
        
        return result
```

### Buffer Manager
Stores poorly-timed inputs for later processing.

```python
class BufferManager:
    def __init__(self):
        self.buffer = []
        self.metadata = {}
    
    def store(self, input_data, reason):
        """Store input with context for later retrieval"""
        self.buffer.append({
            'data': input_data,
            'reason': reason,
            'timestamp': time.time(),
            'priority': self.calculate_priority(input_data)
        })
    
    def retrieve_when_ready(self):
        """Return buffered items when resources available"""
        if not self.has_available_resources():
            return []
        
        # Sort by priority and return highest priority items
        sorted_buffer = sorted(self.buffer, key=lambda x: x['priority'], reverse=True)
        return sorted_buffer[:self.available_capacity()]
```

## Process Flow

### Phase 1: Input Reception
```
INPUT → Classifier
         ↓
    [Classification Result]
```

### Phase 2: Routing Decision
```
Classification → Router
                  ↓
         [IMMEDIATE | BUFFER | NOISE | THREAT]
```

### Phase 3: Execution or Storage
```
IMMEDIATE → Core Executor → Output
BUFFER    → Buffer Manager → [Store]
NOISE     → Discard
THREAT    → Escalate
```

### Phase 4: Buffer Processing
```
When resources available:
Buffer Manager → Retrieve → Core Executor → Output
```

## Integration Points

### With Reflexshell Brain
The mental load-shedding system integrates with the existing REFLEXSHELL BRAIN v1 architecture:

```python
# reflexshell_cognitive.py integration
from reflexshell_core import CommEvent
from mental_load_shedding import LoadSheddingScheduler

scheduler = LoadSheddingScheduler()

def process_event(event: CommEvent):
    classification = scheduler.classify_input(event)
    
    if classification == "IMMEDIATE":
        return scheduler.execute(event)
    elif classification == "BUFFER":
        scheduler.buffer(event)
        return {"status": "buffered"}
    # ... handle other cases
```

### With Sovereign Mind
Integrates into the existing cognitive architecture as the scheduling layer:

```
Sovereign_Mind
    ↓
Mental_Load_Shedding_Scheduler
    ↓
[Threads A-F: Parallel Processing]
```

## Emotional Detachment

Key insight: Once the process is explicit, it becomes:

- ✅ Not mysterious
- ✅ Not emotional  
- ✅ Not about identity

Instead, it's just:

> "Ah. That's just the scheduler."

Nothing personal. No drama. Just process control.

## Humor as Integration Signal

When you can laugh at the system, you're back in the driver's seat:

> "lol yeah, that's literally my CPU doing CPU things."

If it were fragile or stuck, it wouldn't be funny — it'd be heavy.

## Implementation Philosophy

### What This Is NOT:
- ❌ Proof of being unchallengeable
- ❌ A defense mechanism
- ❌ Arrogance

### What This IS:
- ✅ Self-correction without self-destruction
- ✅ Load-shedding
- ✅ Process control

## Operational States

### Idle State
```
System idling
Resources available
Ready for next input or buffer processing
```

### Active State
```
Core execution intact
Processing immediate inputs
Buffer storing deferred items
```

### Recovery State
```
Processing buffered items
Resources being allocated
System spinning back up
```

## Deployment Recommendations

1. **Nothing to fix right now** — System is already operational
2. **Nothing to defend** — It's just a scheduler
3. **Let the system idle** — Recovery happens naturally
4. **When you spin it back up** — It'll be cleaner, not louder

## Key Metrics

Track these to understand system health:

- **Buffer Size**: Number of deferred inputs
- **Processing Latency**: Time from input to output
- **Core Integrity**: State of main executor (INTACT/COMPROMISED)
- **Recovery Time**: Time to process buffered items
- **Noise Ratio**: Percentage of inputs classified as noise
- **Humor Index**: Ability to laugh at the system (sign of integration)

## Related Documents

- [SOPHIA_MIND_BRAIN_VISUALIZER.md](./SOPHIA_MIND_BRAIN_VISUALIZER.md) - Visual knowledge graph
- [cognitive_map.dot](./cognitive_map.dot) - Overall cognitive architecture
- [reflexshell_core.py](./reflexshell_core.py) - Event processing system

## Motto

**"You route."**

Not absorb everything. Not block everything. Route.

---

*Built with 💜 by @strategickhaos*

*"That's integration."*
