# Emotion Compiler Documentation

## Overview

The Emotion Compiler is a system for processing emotions as source code, treating them as runtime events (interrupts) rather than identity truths. It compiles emotions into safe, bounded protocols that prevent regret bugs.

## Core Concepts

### Emotions as Signals

Emotions are structured telemetry packets, not verdicts. Each emotion is parsed into tokens and compiled into an action plan with guards.

### The Compiler Model

1. **Emotion = an event packet (telemetry)**
   - Not a verdict, but a structured message
   - Contains: name, intensity, trigger, body sensations, context, timestamp

2. **Parse into tokens**
   - Emotion type (ANGER, FEAR, SADNESS, JOY, SHAME, CALM)
   - Intensity level (0.0 to 1.0)
   - Trigger identification
   - Context flags (fatigue, stakes, etc.)

3. **Compile to action plan with guards**
   - Not "what I feel" → "what I do"
   - But "what I feel" → "what protocol runs"

## Core Invariant

**No irreversible action during high-intensity states.**

This single rule prevents 95% of regret bugs.

## Primitive Operations

- **ACK()** — acknowledge the interrupt (prevents escalation)
- **BUFFER(t)** — don't decide while hot
- **ANCHOR()** — check invariants ("does it compile?")
- **QUERY()** — ask for missing variables
- **PATCH()** — change environment / inputs
- **EXEC()** — act, but only after guard checks
- **THREAT_MODEL()** — analyze potential threats
- **REWRITE()** — reframe the situation
- **DENY_INPUT()** — reject low-signal input
- **SCOPE_CAP()** — limit scope of action

## Routing Rules

### Anger

**Hot anger** (high intensity or fatigue):
- `BUFFER(30min)` + `ANCHOR()`
- `DENY_INPUT(type="framing")`
- Defer decisions, return later with a diff

**Cool anger** (moderate intensity):
- `QUERY("what exactly is wrong?")`
- `PATCH("fix one concrete thing")`
- Convert to one repair task

### Fear

- `THREAT_MODEL()`
- `QUERY("worst case + likelihood + mitigation")`
- `BUFFER(15min)` if hot
- Convert uncertainty to threat model + mitigation list

### Sadness

- `PATCH(resource="food/water/sleep")`
- `PATCH(connection="trusted person or safe activity")`
- Signals depletion or loss - restore resources before analysis

### Joy

- `EXEC(mode="build")`
- `SCOPE_CAP(limit="one deliverable")`
- Greenlight to ship, but don't over-expand

### Shame

- `REWRITE(frame="data, not identity")`
- `PATCH(next_step="small win")`
- Convert to a small, measurable next step

## Usage

### Basic Example

```python
from emotion_compiler import EmotionCompiler, EmotionEvent, Emotion

# Create compiler
compiler = EmotionCompiler()

# Create emotion event
event = EmotionEvent(
    emotion=Emotion.ANGER,
    intensity=0.85,
    trigger="weakness_framing",
    body=["tight jaw", "heat"],
    context={"fatigue": "high"}
)

# Compile to action plan
plan = compiler.compile(event)

# Examine the plan
print(f"Classification: {plan.classification}")
print(f"Actions: {[f'{a.op}({a.args})' for a in plan.actions]}")
print(f"Notes: {plan.notes}")
```

### Output

```
Classification: ANGRY_HOT
Actions: ['ACK({})', 'ANCHOR({})', "BUFFER({'minutes': '30'})", "DENY_INPUT({'type': 'framing'})"]
Notes: ['Defer decisions. Reject low-signal input. Return later with a diff.']
```

## Advanced Usage

### Event Logging

For analytics and pattern recognition:

```python
import json
from datetime import datetime

# Log event
with open('events.log', 'a') as f:
    event_data = {
        'timestamp': datetime.now().isoformat(),
        'emotion': event.emotion.value,
        'intensity': event.intensity,
        'trigger': event.trigger,
        'body': event.body,
        'context': event.context
    }
    f.write(json.dumps(event_data) + '\n')

# Log plan
with open('plans.log', 'a') as f:
    plan_data = {
        'timestamp': datetime.now().isoformat(),
        'classification': plan.classification,
        'actions': [{'op': a.op, 'args': a.args} for a in plan.actions],
        'notes': plan.notes
    }
    f.write(json.dumps(plan_data) + '\n')
```

Later, you can analyze patterns like "what triggers hot anger most?"

### Custom Compiler Configuration

```python
# Adjust hot threshold
compiler = EmotionCompiler()
compiler.hot_threshold = 0.8  # Only treat 0.8+ as hot

# Disable hot state guardrail (not recommended)
compiler.no_irreversible_when_hot = False
```

## Why This Works

1. **Treats emotions as signals, not "truth"**
   - Emotions provide information, not commands
   - They're data to be processed, not identity statements

2. **Turns "feeling" into procedure, not identity**
   - Instead of "I am angry" → "Anger interrupt detected"
   - Instead of "I should..." → "Protocol ANGRY_HOT activates"

3. **Preserves core rule: compute first, decide later**
   - All emotions start with ACK + ANCHOR
   - Hot states trigger BUFFER before action
   - Guards prevent irreversible actions

## Architecture Extensions

### State Machine Mode (Future Enhancement)

Instead of pure rule-based routing, you could implement:

- **Modes**: BUILD / RECOVERY / DEFENSE / PLAY
- **Transitions**: Based on emotion patterns
- **Guards**: Mode-specific constraints
- **Hooks**: Integrate with boot digest, logging systems

### Integration Points

- **Boot Digest**: Emotion state as health metric
- **Performance System**: Correlation between emotions and productivity
- **Observability**: Real-time emotion state dashboard
- **Alerting**: Patterns that indicate burnout or sustained stress

## Best Practices

1. **Always log events and plans** for later analysis
2. **Trust the buffer** - waiting 15-30 minutes during hot states prevents most mistakes
3. **Anchor frequently** - check invariants before major decisions
4. **Small patches** - prefer many small actions over one large change
5. **Review patterns** - weekly analysis of what triggers which emotions

## Testing

Run the test suite:

```bash
python3 test_emotion_compiler.py
```

## API Reference

### Classes

#### `Emotion(Enum)`
Enumeration of emotion types:
- `ANGER`
- `FEAR`
- `SADNESS`
- `JOY`
- `SHAME`
- `CALM`

#### `EmotionEvent`
Dataclass representing an emotion event.

**Fields:**
- `emotion: Emotion` - Type of emotion
- `intensity: float` - Intensity from 0.0 to 1.0
- `trigger: str` - Short label for what triggered the emotion
- `body: List[str]` - Physical sensations (optional)
- `context: Dict[str, str]` - Contextual information (optional)
- `ts: float` - Timestamp (auto-generated)

#### `Action`
Dataclass representing an action to take.

**Fields:**
- `op: str` - Operation name
- `args: Dict[str, str]` - Arguments for the operation (optional)

#### `Plan`
Dataclass representing a compiled action plan.

**Fields:**
- `classification: str` - Emotion state classification
- `actions: List[Action]` - Ordered list of actions
- `notes: List[str]` - Explanatory notes (optional)

#### `EmotionCompiler`
Main compiler class.

**Methods:**
- `__init__()` - Initialize compiler with default settings
- `compile(e: EmotionEvent) -> Plan` - Compile emotion event into action plan
- `_is_hot(e: EmotionEvent) -> bool` - Determine if emotion is in hot state

**Attributes:**
- `no_irreversible_when_hot: bool` - Guardrail flag (default: True)
- `hot_threshold: float` - Intensity threshold for hot state (default: 0.75)

## Examples

See the `__main__` block in `emotion_compiler.py` for comprehensive examples of all emotion types and states.

## License

Part of the Strategickhaos Sovereignty Architecture.
