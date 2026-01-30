# FlameLang Hello World Example

This directory contains a "Hello, World!" example program in FlameLang's JSON-based module representation format.

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

FlameLang is a sovereign symbolic shell system designed as part of the Strategickhaos Sovereignty Architecture. This JSON module format represents a structured code representation layer. For more information about FlameLang, see the [FlameLang Specification](../../FLAMELANG_SPECIFICATION.md).

## JSON Format

The JSON format represents a structured module definition with the following key types:

- **Module**: Top-level container with name, version, and items
- **Extern**: External function declarations
- **FnDef**: Function definitions with parameters, return type, and body
- **Block**: Statement blocks
- **Call**: Function call expressions
- **Const**: Constant values (String, Number, etc.)
- **Return**: Return statements

## Expected Behavior

If processed by a compatible interpreter or compiler, this program would output:
```
Hello, FlameLang!
```

## Usage

This JSON file serves as:
1. A structured module definition for FlameLang programs
2. An example of the JSON-based code representation format
3. A reference for tools that may process FlameLang modules
4. Documentation of the module structure

## Sovereignty Note

This example demonstrates FlameLang's approach to sovereign code representation, where the program structure is explicitly defined in a human-readable and machine-processable format, maintaining transparency and control over the execution model.

🔥 Reignite.
