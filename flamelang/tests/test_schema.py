#!/usr/bin/env python3
"""
FlameIR v0.1.0 Schema Test Suite

Tests the FlameIR schema against valid and invalid documents to ensure
correctness and robustness of the specification.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema not installed. Install with: pip install jsonschema")
    sys.exit(1)


def load_schema():
    """Load the FlameIR v0.1.0 schema."""
    schema_path = Path(__file__).parent.parent / "schemas" / "flame-ir-v0.1.0.json"
    with open(schema_path) as f:
        return json.load(f)


def test_valid_documents():
    """Test that valid documents pass validation."""
    schema = load_schema()
    validator = Draft7Validator(schema)
    
    test_cases = [
        # Simple constant
        {
            "Const": {"Int": 42}
        },
        # Variable reference
        {
            "Var": {"name": "x"}
        },
        # Binary operation
        {
            "BinOp": {
                "op": "Add",
                "left": {"Const": {"Int": 1}},
                "right": {"Const": {"Int": 2}}
            }
        },
        # Function call
        {
            "Call": {
                "target": "print",
                "args": [{"Const": {"String": "hello"}}]
            }
        },
        # Return statement
        {
            "Return": {
                "value": {"Const": "Unit"}
            }
        },
        # Module with empty items
        {
            "Module": {
                "name": "empty",
                "version": "0.1.0",
                "items": []
            }
        },
        # All primitive types
        {"Const": {"Int": 42}},
        {"Const": {"Float": 3.14}},
        {"Const": {"Bool": True}},
        {"Const": {"String": "text"}},
        {"Const": "Unit"},
        # All binary operators
        *[{
            "BinOp": {
                "op": op,
                "left": {"Const": {"Int": 1}},
                "right": {"Const": {"Int": 2}}
            }
        } for op in ["Add", "Sub", "Mul", "Div", "Mod", "Eq", "Ne", "Lt", "Le", "Gt", "Ge", "And", "Or"]],
        # Function type
        {
            "FnDef": {
                "name": "identity",
                "params": [{
                    "name": "f",
                    "param_type": {
                        "Fn": {
                            "params": ["Int"],
                            "return": "Int"
                        }
                    }
                }],
                "return_type": {
                    "Fn": {
                        "params": ["Int"],
                        "return": "Int"
                    }
                },
                "body": {
                    "Return": {
                        "value": {"Var": {"name": "f"}}
                    }
                }
            }
        },
        # Nested function types
        {
            "FnDef": {
                "name": "higher_order",
                "params": [{
                    "name": "f",
                    "param_type": {
                        "Fn": {
                            "params": [{
                                "Fn": {
                                    "params": ["Int"],
                                    "return": "Int"
                                }
                            }],
                            "return": "Int"
                        }
                    }
                }],
                "return_type": "Int",
                "body": {
                    "Return": {
                        "value": {"Const": {"Int": 0}}
                    }
                }
            }
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        errors = list(validator.iter_errors(test_case))
        if errors:
            print(f"❌ Test case {i} failed (expected valid):")
            print(f"   {json.dumps(test_case, indent=2)}")
            for error in errors:
                print(f"   Error: {error.message}")
            failed += 1
        else:
            passed += 1
    
    return passed, failed


def test_invalid_documents():
    """Test that invalid documents fail validation."""
    schema = load_schema()
    validator = Draft7Validator(schema)
    
    test_cases = [
        # Missing required fields
        {"Module": {"name": "test"}},  # Missing items and version
        {"FnDef": {"name": "test"}},  # Missing params, return_type, body
        {"BinOp": {"op": "Add"}},  # Missing left and right
        {"Call": {"target": "f"}},  # Missing args
        {"Return": {}},  # Missing value
        {"Var": {}},  # Missing name
        {"Let": {"name": "x"}},  # Missing value
        # Invalid types
        {"Const": {"Int": "not a number"}},
        {"Const": {"Float": True}},
        {"Const": {"Bool": "not a boolean"}},
        # Invalid operator
        {"BinOp": {
            "op": "InvalidOp",
            "left": {"Const": {"Int": 1}},
            "right": {"Const": {"Int": 2}}
        }},
        # Wrong version
        {"Module": {
            "name": "test",
            "version": "0.2.0",  # Should be 0.1.0
            "items": []
        }},
        # Invalid structure
        {"InvalidNode": {}},
        # Empty object
        {},
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        errors = list(validator.iter_errors(test_case))
        if not errors:
            print(f"❌ Test case {i} passed (expected invalid):")
            print(f"   {json.dumps(test_case, indent=2)}")
            failed += 1
        else:
            passed += 1
    
    return passed, failed


def main():
    """Run all tests."""
    print("🔥 FlameIR v0.1.0 Schema Test Suite\n")
    
    print("=" * 60)
    print("Testing Valid Documents")
    print("=" * 60)
    valid_passed, valid_failed = test_valid_documents()
    print(f"✅ Passed: {valid_passed}")
    if valid_failed > 0:
        print(f"❌ Failed: {valid_failed}")
    print()
    
    print("=" * 60)
    print("Testing Invalid Documents")
    print("=" * 60)
    invalid_passed, invalid_failed = test_invalid_documents()
    print(f"✅ Rejected correctly: {invalid_passed}")
    if invalid_failed > 0:
        print(f"❌ Incorrectly accepted: {invalid_failed}")
    print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    total_passed = valid_passed + invalid_passed
    total_failed = valid_failed + invalid_failed
    total_tests = total_passed + total_failed
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    
    if total_failed == 0:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {total_failed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
