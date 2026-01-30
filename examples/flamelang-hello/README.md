# FlameLang Hello World Example

This directory contains a "Hello, World!" example program written in FlameLang's JSON-based intermediate representation (IR) format.

## File Structure

- `hello.json` - The FlameLang module definition in JSON format

## Module Structure

The JSON file represents a FlameLang module with the following components:

### Module Definition
```json
{
  "Module": {
    "name": "hello",
    "version": "0.1.0",
    "items": [...]
  }
}
```

### Extern Declaration
Declares an external function `print` that takes a String parameter and returns Unit (void):
```json
{
  "Extern": {
    "name": "print",
    "params": ["String"],
    "return_type": "Unit"
  }
}
```

### Function Definition
Defines the `main` function that calls `print` with "Hello, FlameLang!" and returns:
```json
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
                {
                  "Const": {
                    "String": "Hello, FlameLang!"
                  }
                }
              ]
            }
          },
          {
            "Return": {
              "value": null
            }
          }
        ]
      }
    }
  }
}
```

## About FlameLang

FlameLang is a sovereign symbolic shell system designed as part of the Strategickhaos Sovereignty Architecture. For more information, see the [FlameLang Specification](../../FLAMELANG_SPECIFICATION.md).

## JSON Schema

The JSON format represents an Abstract Syntax Tree (AST) or Intermediate Representation (IR) of FlameLang code with the following key types:

- **Module**: Top-level container with name, version, and items
- **Extern**: External function declarations
- **FnDef**: Function definitions with parameters, return type, and body
- **Block**: Statement blocks
- **Call**: Function call expressions
- **Const**: Constant values (String, Number, etc.)
- **Return**: Return statements

## Expected Output

When executed by a FlameLang interpreter/compiler, this program should output:
```
Hello, FlameLang!
```

## Usage

This JSON file can be:
1. Parsed by a FlameLang compiler to generate executable code
2. Interpreted directly by a FlameLang runtime
3. Used as input for code generation or transformation tools
4. Validated against FlameLang's JSON schema

## Sovereignty Note

This example demonstrates FlameLang's approach to sovereign code representation, where the program structure is explicitly defined in a human-readable and machine-processable format, maintaining transparency and control over the execution model.

🔥 Reignite.
