# DEMYSTIFIER CLI - INV-091

A semantic linter that validates claims against grounding checks.

**Not hype. Not mythology. Just validation.**

## Overview

The DEMYSTIFIER CLI is a tool that analyzes text claims and validates them against six grounding checks:

1. **MEASURABLE** - Can you assign a number to it?
2. **FALSIFIABLE** - What would prove it wrong?
3. **BOUNDED** - Where does it start and end?
4. **OBSERVABLE** - Can someone else verify it?
5. **ACTIONABLE** - What do you DO with this?
6. **OWNABLE** - Who is responsible?

## Installation

No installation required. The tool is a standalone Python script that uses only standard library modules.

Requirements:
- Python 3.7 or higher

## Usage

### Basic Usage

Analyze a single claim:

```bash
python3 demystifier.py "I can manifest abundance"
```

### Demo Mode

Run without arguments to see demo examples:

```bash
python3 demystifier.py
```

### File Input Mode

Analyze multiple claims from a file (one claim per line):

```bash
python3 demystifier.py --file claims.txt
```

### Interactive Mode

Enter claims interactively:

```bash
python3 demystifier.py --interactive
```

Type claims one at a time, press Enter after each. Type `quit` or `exit` to stop.

### JSON Output

Get machine-readable JSON output:

```bash
python3 demystifier.py --json "I will build a CLI tool within 2 hours"
```

### Quiet Mode

Show only the verdict for each claim:

```bash
python3 demystifier.py --quiet "I am a lightworker"
```

Useful for batch processing with `--file`:

```bash
python3 demystifier.py --file claims.txt --quiet
```

## Output Format

### Text Output (Default)

```
══════════════════════════════════════════════════════════════════════
🔥 DEMYSTIFIER REPORT - INV-091
══════════════════════════════════════════════════════════════════════
INPUT: "I can manifest abundance"
TIME:  2026-01-19T07:31:50.025917

📍 DETECTIONS:
   [POWER_CLAIM] "i can manifest"
   [ABSTRACT_VERB] "manifest"

🔄 TRANSLATIONS:
   "i can manifest" → I can plan and execute (process: goal→action→outcome)
   "manifest" → plan_and_execute()

✓ GROUNDING CHECKS:
   ⚠️ WARN MEASURABLE
      └─ No explicit metrics found
   ⚠️ WARN FALSIFIABLE
      └─ No explicit test conditions
   ⚠️ WARN BOUNDED
      └─ No explicit boundaries
   ⚠️ WARN OBSERVABLE
      └─ Observability unclear
   ❌ FAIL ACTIONABLE
      └─ Uses abstract/non-operational verbs
   ✅ PASS OWNABLE
      └─ Has explicit human owner

──────────────────────────────────────────────────────────────────────
VERDICT: ❌ REJECTED - Failed grounding checks
──────────────────────────────────────────────────────────────────────
GROUNDED VERSION: I can plan and execute (process: goal→action→outcome)

📋 NEXT STEPS:
   → [MEASURABLE] Add: count, duration, frequency, or other metric
   → [FALSIFIABLE] Add: 'This fails if...'
   → [BOUNDED] Add: scope, duration, or domain limits
   → [OBSERVABLE] Specify what external evidence would look like
   → [ACTIONABLE] Replace with concrete verbs: do, make, create, build
══════════════════════════════════════════════════════════════════════
```

## Detection Categories

The tool detects the following patterns in text:

- **IDENTITY_CLAIM** - Claims about personal identity (e.g., "I am a lightworker")
- **DESTINY_FRAME** - Appeals to fate or cosmic intention (e.g., "The universe wants...")
- **POWER_CLAIM** - Claims of special abilities (e.g., "I can manifest...")
- **UNBOUNDED_NOUN** - Use of infinite/unlimited concepts (e.g., "infinite potential")
- **ABSTRACT_VERB** - Use of vague action words (e.g., "manifest", "align", "channel")

## Translation Examples

The tool automatically suggests grounded alternatives:

| Mystical Phrase | Grounded Translation |
|----------------|---------------------|
| "I am a lightworker" | "I help people (metric: count_helped)" |
| "I can manifest" | "I can plan and execute (process: goal→action→outcome)" |
| "The universe wants" | "I want (owner: self)" |
| "infinite potential" | "large but finite capacity (bound: measurable_limit)" |
| "everything is connected" | "systems have dependencies (model: Graph{nodes,edges})" |

## Verdict Types

- **✅ GROUNDED** - All checks passed
- **⚠️ PARTIAL** - Some checks inconclusive
- **⚠️ NEEDS WORK** - Multiple warnings (3+)
- **❌ REJECTED** - Failed grounding checks

## Testing

Run the test suite:

```bash
python3 test_demystifier.py
```

The test suite validates:
- Pattern detection accuracy
- Translation correctness
- All six grounding checks
- Edge cases and special inputs
- Full pipeline functionality

## Examples

### Mystical Claim (Rejected)

```bash
python3 demystifier.py "I am a lightworker channeling universal energy"
```

Result: ❌ REJECTED - Multiple failed checks (unbounded, abstract, not observable)

### Grounded Claim (Passes)

```bash
python3 demystifier.py "I will build 5 API endpoints within 8 hours for our team"
```

Result: ✅ GROUNDED or ⚠️ PARTIAL - Most checks pass

### Batch Processing

```bash
# Create claims file
cat > my_claims.txt << EOF
I am meant to be a leader
I will complete 10 tasks by Friday at 5pm
The universe guides my decisions
I can manifest success
EOF

# Process all claims
python3 demystifier.py --file my_claims.txt --quiet
```

## Philosophy

The DEMYSTIFIER enforces **grounded thinking**:

- Claims should be **measurable** with concrete metrics
- Claims should be **falsifiable** with clear failure conditions
- Claims should be **bounded** in scope and time
- Claims should be **observable** by external parties
- Claims should be **actionable** with concrete steps
- Claims should have **clear ownership** by humans

**Not hype. Not mythology. Just validation.**

## License

Part of the Sovereignty Architecture project.

## Related

- INV-091: Semantic linter for mystical thinking
- Part of the StrategicKhaos DAO toolkit
