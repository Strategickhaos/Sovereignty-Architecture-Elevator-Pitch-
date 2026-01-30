# 🔥 FlameIR v0.1.0 - FlameLang Intermediate Representation

## Overview

FlameIR v0.1.0 is the **FROZEN** Intermediate Representation (IR) specification for FlameLang, the sovereign symbolic language developed by Strategickhaos. This specification defines a typed, structured format for representing FlameLang programs in a machine-readable form suitable for compilation, interpretation, and analysis.

**⚠️ IMPORTANT: This is a FROZEN specification. No modifications are permitted without a version bump.**

## Schema Location

- **Schema File**: `flamelang/schemas/flame-ir-v0.1.0.json`
- **Schema ID**: `https://strategickhaos.ai/flamelang/ir/v0.1.0`
- **JSON Schema Version**: Draft-07

## Core Concepts

### Type System

FlameIR supports a simple but powerful type system:

- **Primitive Types**:
  - `Int` - Integer numbers
  - `Float` - Floating-point numbers
  - `Bool` - Boolean values (true/false)
  - `String` - Text strings
  - `Unit` - The unit type (similar to void)

- **Function Types**:
  - `Fn` - Function type with parameters and return type
  - Example: `{ "Fn": { "params": ["Int", "Int"], "return": "Bool" } }`

### IR Node Types

FlameIR programs are represented as a tree of nodes, each representing a different language construct:

#### Module
The top-level container for a FlameLang program.

```json
{
  "Module": {
    "name": "my_program",
    "version": "0.1.0",
    "items": [...]
  }
}
```

#### FnDef (Function Definition)
Defines a function with parameters, return type, and body.

```json
{
  "FnDef": {
    "name": "add",
    "params": [
      { "name": "a", "param_type": "Int" },
      { "name": "b", "param_type": "Int" }
    ],
    "return_type": "Int",
    "body": {...}
  }
}
```

#### Block
A sequence of statements executed in order.

```json
{
  "Block": {
    "statements": [...]
  }
}
```

#### Let (Variable Binding)
Creates a new variable binding.

```json
{
  "Let": {
    "name": "x",
    "value": {...},
    "let_type": "Int"
  }
}
```

#### Const (Constant Value)
Represents a literal constant value.

```json
{
  "Const": { "Int": 42 }
}
{
  "Const": { "String": "Hello" }
}
{
  "Const": { "Bool": true }
}
{
  "Const": "Unit" }
}
```

#### Call (Function Call)
Invokes a function with arguments.

```json
{
  "Call": {
    "target": "print",
    "args": [...]
  }
}
```

#### Return
Returns a value from a function.

```json
{
  "Return": {
    "value": {...}
  }
}
```

#### Extern (External Declaration)
Declares an external function signature.

```json
{
  "Extern": {
    "name": "print_int",
    "params": ["Int"],
    "return_type": "Unit"
  }
}
```

#### Var (Variable Reference)
References a previously defined variable.

```json
{
  "Var": {
    "name": "x"
  }
}
```

#### BinOp (Binary Operation)
Performs a binary operation on two operands.

```json
{
  "BinOp": {
    "op": "Add",
    "left": {...},
    "right": {...}
  }
}
```

### Binary Operators

FlameIR supports the following binary operators:

- **Arithmetic**: `Add`, `Sub`, `Mul`, `Div`, `Mod`
- **Comparison**: `Eq`, `Ne`, `Lt`, `Le`, `Gt`, `Ge`
- **Logical**: `And`, `Or`

## Examples

### Hello World

```json
{
  "Module": {
    "name": "hello_world",
    "version": "0.1.0",
    "items": [
      {
        "FnDef": {
          "name": "main",
          "params": [],
          "return_type": "Unit",
          "body": {
            "Block": {
              "statements": [
                {
                  "Call": {
                    "target": "print",
                    "args": [
                      { "Const": { "String": "Hello, World!" } }
                    ]
                  }
                },
                { "Return": { "value": { "Const": "Unit" } } }
              ]
            }
          }
        }
      }
    ]
  }
}
```

See `flamelang/examples/` for more comprehensive examples:
- `hello_world.json` - Simple program printing a message
- `arithmetic.json` - Arithmetic operations and function calls
- `function_types.json` - Higher-order functions with function types

## Validation

To validate a FlameIR document against the schema, use any JSON Schema validator:

### Using Node.js (ajv)

```bash
npm install -g ajv-cli
ajv validate -s flamelang/schemas/flame-ir-v0.1.0.json -d your-program.json
```

### Using Python (jsonschema)

```python
import json
from jsonschema import validate

with open('flamelang/schemas/flame-ir-v0.1.0.json') as f:
    schema = json.load(f)

with open('your-program.json') as f:
    program = json.load(f)

validate(instance=program, schema=schema)
print("✅ Valid FlameIR v0.1.0 document")
```

## Design Principles

1. **Frozen Specification**: This is version 0.1.0. Any modifications require a version bump.
2. **Type Safety**: Every expression has an associated type for static analysis.
3. **Simplicity**: The IR is intentionally minimal, focusing on core language constructs.
4. **JSON-based**: Uses JSON for broad tooling support and human readability.
5. **Composability**: All constructs can be nested to form complex programs.

## Integration with FlameLang

FlameIR serves as the intermediate representation in the FlameLang compilation pipeline:

```
FlameLang Source Code
         ↓
    [Parser]
         ↓
   FlameIR v0.1.0  ← You are here
         ↓
  [Optimizer/Analyzer]
         ↓
   [Code Generator]
         ↓
  Target Code (LLVM IR, WebAssembly, etc.)
```

## Version History

- **v0.1.0** (2026-01-30): Initial frozen specification
  - Core type system
  - Basic control flow constructs
  - Function definitions and calls
  - Binary operations
  - External function declarations

## Future Considerations

While this specification is frozen, future versions may include:
- Pattern matching constructs
- More complex type features (generics, traits)
- Structured data types (structs, enums)
- Control flow (if/else, loops)
- Memory management primitives

## License

This specification is part of the Strategickhaos Sovereignty Architecture project.

See [LICENSE](../LICENSE) for details.

---

**🔥 Reignite.**

*Built by Strategickhaos DAO LLC | Part of the FlameLang Sovereign Language System*
