# STRESS-3.36: Count Non-Space/Punctuation Characters

## Overview

This is an implementation of zyBooks IT-145 Lab 3.36, which demonstrates the fundamental signal processing pattern: **iterate, filter, count**.

## Problem Statement

Write a program that counts the "meaningful" characters in a line of text by filtering out noise characters (spaces and simple punctuation).

## Implementation

**File**: `LabProgram.java`

The program:
1. Reads one line of user input using Scanner
2. Iterates through each character (for-loop from index 0 to length-1)
3. Filters out noise characters: space, '.', '!', ','
4. Counts remaining signal characters
5. Prints the final count

## Usage

### Compile and Run

```bash
# Compile
javac LabProgram.java

# Run with input
echo "Listen, Mr. Jones, calm down." | java LabProgram
```

### Expected Output

```
21
```

## Test Vectors

All test cases pass successfully:

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| zyBooks example | `Listen, Mr. Jones, calm down.` | 21 | ✓ |
| Basic word | `hello` | 5 | ✓ |
| Simple sentence | `Hello, world!` | 10 | ✓ |
| Trailing spaces | `   test  ` | 4 | ✓ |
| Punctuation only | `.,!,!` | 0 | ✓ |
| Mixed alphanum | `A1B2 C3!` | 6 | ✓ |
| Empty line | `` | 0 | ✓ |
| Unicode chars | `Héllo wörld!` | 10 | ✓ |

## Conceptual Framework

This lab implements the universal pattern found across multiple domains:

- **Ramanujan**: Iterate through mathematical patterns, filter noise (invalid theorems), count signal (valid insights)
- **Einstein**: Iterate through physics assumptions, filter noise (absolute space/time), count signal (invariants)
- **Signal Processing**: Iterate through data stream, filter noise, measure meaningful activity
- **EEG Analysis**: Iterate through neural firing, filter background noise, count meaningful activity

The same cognitive architecture applies across all domains: **scan → filter → measure**.

## DNA Encoding

```
ATG-CAT-GAT-ACC-TCG
```

- **ATG**: program_start
- **CAT**: init_scanner_buffer
- **GAT**: scan_loop_over_chars
- **ACC**: noise_filter_conditional
- **TCG**: terminate_and_print

## Notes

- Single pass over input (O(n) time complexity)
- Constant space usage (O(1) space complexity)
- Scanner resource properly closed to prevent leaks
- Works with Unicode characters (counts as signal)
- Compatible with Java 8+ (uses no preview features)
