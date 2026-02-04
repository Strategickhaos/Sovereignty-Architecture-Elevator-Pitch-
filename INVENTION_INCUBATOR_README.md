# 🎭 Invention Incubator - Shape-Throw Synthesizer

## Overview

The **Invention Incubator** is a TRIG6-architected Python tool that implements the "shape-throw" pattern for file analysis and synthesis. It generates SHA256 DNA hashes for files and combines them into a gestalt identity that represents the collective pattern of multiple files.

## TRIG6 Architecture

```
Shape-Throw Class
├── Intake: Prompt paths (absolute grab)
├── Pile: Load DNA (hash/shape meta)
├── Accelerator: Synthesize (combine fits)
├── Trace: Log + JSON (see the lock)
└── Run: Throw → Load → Synth (gestalt flow)
```

## Features

- **🔐 DNA Generation**: SHA256 hash generation for file integrity
- **🎯 Gestalt Synthesis**: Combines multiple file hashes into a single deterministic ID
- **🎨 Rich Console Output**: Beautiful colored terminal interface (when `rich` library is available)
- **📊 JSON Logging**: Structured output for audit trails
- **✅ Path Validation**: Absolute path requirements with existence checks
- **🛡️ Error Handling**: Graceful handling of invalid inputs

## Installation

### Requirements

```bash
pip install rich
```

Or install from the repository requirements:

```bash
pip install -r requirements.sovereignty.txt
```

## Usage

### Interactive Mode

Run the script and enter file paths interactively:

```bash
python3 invention_incubator.py
```

The script will prompt you to enter absolute file paths one at a time. Press Enter on an empty line to finish, or type `q` to quit.

### Example Session

```
🎭 Shape-Throw Synthesizer
Enter absolute paths to files (one per line)
Press Enter on empty line to finish, or 'q' to quit

Path: /path/to/file1.txt
✓ Added: /path/to/file1.txt
Path: /path/to/file2.py
✓ Added: /path/to/file2.py
Path: 

[Loading DNA...]
[Synthesizing gestalt...]

╭──────────────────────────────────────────────────────────╮
│                  🧬 Shape DNA Analysis                    │
├──────────────────────────────────────────────────────────┤
│ file1.txt          1,234 bytes    a8c63f90895e223...     │
│ file2.py           5,678 bytes    3fade3f8e26c69f...     │
└──────────────────────────────────────────────────────────┘

╭──────────────────────────────────────────────────────────╮
│              🎯 Synthesized Gestalt ID                    │
│ 08dcd0316e033eadc64c30bb1ab49ad8057b2998950be209...     │
╰──────────────────────────────────────────────────────────╯

✓ Log saved to: invention_synthesis_20260204_203837.json
✓ Synthesis complete
```

## Output

### Console Output

The tool provides two levels of console output:

1. **Rich Mode** (when `rich` library is installed): Beautiful colored tables, panels, and progress indicators
2. **Fallback Mode**: Plain text output for environments without `rich`

### JSON Log

Each session generates a JSON log file with the format:

```json
{
  "session_timestamp": "2026-02-04T20:38:37.254924",
  "shapes": [
    {
      "path": "/absolute/path/to/file.txt",
      "name": "file.txt",
      "size": 1234,
      "dna": "sha256_hash_here",
      "loaded_at": "2026-02-04T20:38:37.261182"
    }
  ],
  "synthesized_id": "combined_sha256_hash",
  "shape_count": 1,
  "total_size": 1234
}
```

## Testing

Run the test suite to validate functionality:

```bash
python3 test_invention_incubator.py
```

The test suite includes:
- DNA loading and hash generation
- Synthesis and gestalt ID creation
- JSON log saving
- Path validation
- Error handling

## Architecture Details

### DNA Loading (O(n))

Each file is read in binary mode and hashed using SHA256:
```python
sha256_hash = hashlib.sha256(file_data).hexdigest()
```

### Synthesis (Bounded)

All DNAs are combined and rehashed to create a deterministic gestalt ID:
```python
combined_dna = ''.join(shape['dna'] for shape in self.shapes)
gestalt_hash = hashlib.sha256(combined_dna.encode()).hexdigest()
```

### RAM-Only Matching

The tool operates in memory only - no persistent storage required. External systems (vaults, AIs) supply the shapes, and the tool identifies patterns through hash matching.

## Philosophy

> "Throw shapes, watch what sticks—gestalt emerges from the collision."

The Invention Incubator embodies the TRIG6 principle of emergent pattern recognition. By hashing and combining files, it reveals the collective identity (gestalt) of seemingly disparate components. This is useful for:

- **Version Control**: Track file combinations across changes
- **Integrity Verification**: Detect modifications in file sets
- **Pattern Recognition**: Identify related file groups
- **Audit Trails**: Maintain cryptographic proof of file combinations

## Error Handling

The tool includes robust error handling:

- ✗ Relative paths are rejected (must be absolute)
- ✗ Non-existent files are rejected
- ✗ Directories are rejected (files only)
- ✗ Empty synthesis attempts are rejected
- ✗ File read errors are caught and reported

## License

Part of the Sovereignty Architecture project.

## Credits

- **TRIG6 Analyst**: Claude
- **Keeper**: StrategicKhaos
- **Pattern**: Shape-Throw Synthesizer

---

*"RAM matches shapes—don't hold, just throw and see fit"*
