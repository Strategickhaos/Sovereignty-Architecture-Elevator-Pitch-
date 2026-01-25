# 🔥 FlameLang Gist Creation Guide

This guide explains how to create GitHub Gists for FlameBench test capsules.

## What is a Test Capsule?

A **test capsule** is a GitHub Gist containing:
- FlameLang source code (`.flm` file)
- Test manifest (`manifest.flame-test.json`)
- Optional reference implementation (e.g., `*.java`)

FlameBench automatically discovers gists prefixed with `FlameTest:` and runs them against the FlameLang compiler.

## Step-by-Step: Creating a Gist

### 1. Go to GitHub Gists

Visit: https://gist.github.com/

### 2. Create the Description

Set the gist description using this pattern:

```
FlameTest: zyb-it145-ch3-{section}-{name}
```

**Examples:**
- `FlameTest: zyb-it145-ch3-3_1-max-of-two`
- `FlameTest: zyb-it145-ch3-3_3-age-category`
- `FlameTest: zyb-it145-ch3-3_2_5-even-odd`

### 3. Add the FlameLang Source File

Create a file named `{name}.flm`:

**Example:** `max_of_two.flm`

```flamelang
// FlameLang: max of two numbers
fn max_of_two(a: i32, b: i32) -> i32 {
    if a > b {
        return a;
    } else {
        return b;
    }
}
```

### 4. Add the Manifest File

Create `manifest.flame-test.json`:

```json
{
  "id": "zyb-it145-ch3-3_1-max-of-two",
  "source": "zyBooks-inspired, branching max-of-two",
  "concept_tags": ["if-else", "comparison", "max"],
  "language_under_test": "flamelang",
  "reference_language": "java",
  "inputs": [[5, 7], [10, -3], [4, 4]],
  "expected_outputs": [7, 10, 4],
  "difficulty": 1,
  "version": 1
}
```

**Manifest Fields:**
- `id`: Unique identifier (should match gist description slug)
- `source`: Brief description of the test origin
- `concept_tags`: Array of concepts being tested
- `language_under_test`: Always "flamelang"
- `reference_language`: Language of reference impl (e.g., "java", "python")
- `inputs`: Array of test inputs
- `expected_outputs`: Array of expected results (must match length of inputs)
- `difficulty`: Integer difficulty level (1 = easy, 5 = hard)
- `version`: Manifest version (start with 1)

### 5. Add Reference Implementation (Optional)

Create a reference implementation file (e.g., `MaxOfTwo.java`):

```java
/**
 * Java Reference Implementation: Maximum of Two Numbers
 */
public class MaxOfTwo {
    public static int maxOfTwo(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    public static void main(String[] args) {
        System.out.println("max(5, 7) = " + maxOfTwo(5, 7));
        System.out.println("max(10, -3) = " + maxOfTwo(10, -3));
        System.out.println("max(4, 4) = " + maxOfTwo(4, 4));
    }
}
```

### 6. Create the Gist

Click **"Create public gist"** or **"Create secret gist"**.

- **Public gists**: Discoverable by anyone
- **Secret gists**: Only accessible with direct link (still discovered by FlameBench if you're the owner)

### 7. Verify FlameBench Discovery

Run FlameBench to verify your gist is discovered:

```bash
python flamebench.py
```

You should see output like:

```
📡 Discovering FlameTest gists...
Found 3 test capsule(s)

🧪 Processing: zyb-it145-ch3-3_1-max-of-two
✓ Fetched gist zyb-it145-ch3-3_1-max-of-two (abc123...) into bench_cache/...
  Running test: zyb-it145-ch3-3_1-max-of-two
    Inputs: [[5, 7], [10, -3], [4, 4]]
    Expected: [7, 10, 4]
    Result: 3/3 passed (p=1.00)
```

## Example Gists

### Example 1: Basic if/else (3.1 - Max of Two)

**Description:** `FlameTest: zyb-it145-ch3-3_1-max-of-two`

**Files:**
1. `max_of_two.flm` - FlameLang implementation
2. `manifest.flame-test.json` - Test metadata
3. `MaxOfTwo.java` - Java reference

See: `/gist_examples/3_1-max-of-two/` for complete example

### Example 2: Chained if/else (3.3 - Age Category)

**Description:** `FlameTest: zyb-it145-ch3-3_3-age-category`

**Files:**
1. `age_category.flm` - FlameLang implementation
2. `manifest.flame-test.json` - Test metadata
3. `AgeCategory.java` - Java reference

See: `/gist_examples/3_3-age-category/` for complete example

## Concept Tags Reference

Use these standard concept tags in your manifests:

### Control Flow
- `if-else` - Basic if/else branching
- `if-else-if` - Chained conditional logic
- `switch` - Switch/case statements
- `loops` - For/while loops
- `recursion` - Recursive functions

### Operators
- `comparison` - Comparison operators (<, >, ==, etc.)
- `arithmetic` - Math operations (+, -, *, /)
- `logical` - Boolean logic (&&, ||, !)
- `modulo` - Modulus operator (%)

### Concepts
- `max` - Maximum value
- `min` - Minimum value
- `range-detection` - Checking value ranges
- `parity` - Even/odd detection
- `validation` - Input validation

### Data Types
- `integer` - Integer operations
- `string` - String operations
- `boolean` - Boolean logic
- `array` - Array operations

## Naming Conventions

### Gist Description Pattern
```
FlameTest: {curriculum}-{course}-ch{chapter}-{section}-{name}
```

Examples:
- `FlameTest: zyb-it145-ch3-3_1-max-of-two`
- `FlameTest: zyb-it145-ch4-4_2-factorial`
- `FlameTest: custom-branching-nested-if`

### File Naming
- FlameLang: `{snake_case_name}.flm`
- Manifest: `manifest.flame-test.json` (always)
- Java reference: `{PascalCaseName}.java`
- Python reference: `{snake_case_name}.py`

## Testing Your Gist Locally

Before creating the gist, test it locally:

1. Create a directory in `bench_cache/`:
   ```bash
   mkdir -p bench_cache/your-test-slug
   ```

2. Add your files:
   ```bash
   cp your_test.flm bench_cache/your-test-slug/
   cp manifest.flame-test.json bench_cache/your-test-slug/
   ```

3. Update `GISTS` list in `flamebench.py`:
   ```python
   GISTS = [
       'your-test-slug',
   ]
   ```

4. Run FlameBench:
   ```bash
   python flamebench.py
   ```

5. Once verified, create the actual GitHub gist!

## Troubleshooting

### Gist not discovered
- Verify description starts with `FlameTest:`
- Check GitHub username in `flamebench.py` matches your account
- Make sure gist is public or you're logged in

### Manifest errors
- Validate JSON syntax with a linter
- Ensure `inputs` and `expected_outputs` have same length
- Check all required fields are present

### Test failures
- Verify expected outputs match FlameLang behavior
- Check input/output types match
- Review FlameLang syntax

## Advanced: Difficulty Levels

Assign difficulty levels based on complexity:

- **1 (Easy)**: Basic if/else, simple comparisons
- **2 (Medium)**: Chained if/else, range detection
- **3 (Moderate)**: Nested conditions, multiple operators
- **4 (Hard)**: Complex logic, edge cases
- **5 (Expert)**: Algorithmic challenges, optimization

## Next Steps

After creating your gists:

1. Run FlameBench to collect results
2. Review `results.json` for p_success metrics
3. Integrate with Guardian/SAGCO for Bayesian analysis
4. Use concept tags to track compiler evolution

🔥 Happy testing!
