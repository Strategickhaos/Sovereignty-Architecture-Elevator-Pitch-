#!/usr/bin/env python3
"""
FlameIR v0.1.0 Validator

This script validates FlameIR JSON documents against the official schema.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft7Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    print("Warning: jsonschema not installed. Install with: pip install jsonschema")


def load_schema():
    """Load the FlameIR v0.1.0 schema."""
    schema_path = Path(__file__).parent.parent / "schemas" / "flame-ir-v0.1.0.json"
    with open(schema_path) as f:
        return json.load(f)


def validate_flame_ir(document_path, schema=None):
    """
    Validate a FlameIR document against the schema.
    
    Args:
        document_path: Path to the FlameIR JSON document
        schema: Optional schema dict (will load default if not provided)
    
    Returns:
        bool: True if valid, False otherwise
    """
    if schema is None:
        schema = load_schema()
    
    # Load the document first (to check JSON syntax)
    try:
        with open(document_path) as f:
            document = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {document_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    try:
        if HAS_JSONSCHEMA:
            # Use jsonschema for detailed validation
            validator = Draft7Validator(schema)
            errors = list(validator.iter_errors(document))
            
            if errors:
                print(f"❌ Validation failed for {document_path}")
                print(f"\nFound {len(errors)} error(s):\n")
                for i, error in enumerate(errors, 1):
                    print(f"Error {i}:")
                    print(f"  Path: {' -> '.join(str(p) for p in error.path)}")
                    print(f"  Message: {error.message}")
                    print()
                return False
            else:
                print(f"✅ Valid FlameIR v0.1.0 document: {document_path}")
                return True
        else:
            # Warn that full validation is not possible
            print(f"⚠️  Warning: jsonschema not installed - cannot perform schema validation")
            print(f"⚠️  Install with: pip install jsonschema")
            print(f"✅ Document is valid JSON: {document_path}")
            print(f"⚠️  Schema validation was NOT performed")
            return False  # Return False to indicate incomplete validation
            
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False


def validate_all_examples():
    """Validate all example files."""
    examples_dir = Path(__file__).parent.parent / "examples"
    schema = load_schema()
    
    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        return False
    
    example_files = list(examples_dir.glob("*.json"))
    
    if not example_files:
        print("⚠️  No example files found to validate")
        return True
    
    print(f"🔥 Validating {len(example_files)} FlameIR example(s)...\n")
    
    all_valid = True
    for example_file in sorted(example_files):
        if not validate_flame_ir(example_file, schema):
            all_valid = False
        print()
    
    if all_valid:
        print(f"✅ All {len(example_files)} example(s) are valid!")
    else:
        print(f"❌ Some examples failed validation")
    
    return all_valid


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Validate specific file(s)
        schema = load_schema()
        all_valid = True
        
        for file_path in sys.argv[1:]:
            if not validate_flame_ir(Path(file_path), schema):
                all_valid = False
            print()
        
        sys.exit(0 if all_valid else 1)
    else:
        # Validate all examples
        success = validate_all_examples()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
