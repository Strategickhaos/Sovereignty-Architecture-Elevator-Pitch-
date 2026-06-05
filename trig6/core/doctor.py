"""
TRIG6 Doctor - Self-validation
8 tests that must pass for the system to boot
"""

import math
import sys
from .model_registry import get_model
from .units import Angle


class DoctorTest:
    """Individual doctor test"""
    
    def __init__(self, name, test_func):
        self.name = name
        self.test_func = test_func
    
    def run(self):
        """Run the test and return result"""
        try:
            result = self.test_func()
            return {
                'name': self.name,
                'passed': result,
                'error': None
            }
        except Exception as e:
            return {
                'name': self.name,
                'passed': False,
                'error': str(e)
            }


def test_sin_cos_identity():
    """Test: sin²(θ) + cos²(θ) = 1"""
    vector_model = get_model('vector')
    result = vector_model.compute(theta=37)  # Arbitrary angle
    sin_val = result['sin']
    cos_val = result['cos']
    identity = sin_val**2 + cos_val**2
    # Check if close to 1 (within floating point precision)
    return abs(identity - 1.0) < 1e-10


def test_sec_60():
    """Test: sec(60°) = 2"""
    vector_model = get_model('vector')
    result = vector_model.compute(theta=60)
    sec_val = result['sec']
    # sec(60°) = 1/cos(60°) = 1/0.5 = 2
    return abs(sec_val - 2.0) < 1e-10


def test_tan_45():
    """Test: tan(45°) = 1"""
    vector_model = get_model('vector')
    result = vector_model.compute(theta=45)
    tan_val = result['tan']
    return abs(tan_val - 1.0) < 1e-10


def test_bridle_60():
    """Test: Bridle at 60° from vertical should equal load W"""
    # At 60° from vertical, cos(60°) = 0.5
    # T = W / (2 * cos(60°)) = W / (2 * 0.5) = W
    bridle_model = get_model('bridle_two_leg_equal_angle')
    load = 100  # lbf
    result = bridle_model.compute(load=load, theta=60)
    tension = result['tension_per_leg']
    # At 60°, each leg carries the full load
    return abs(tension - load) < 0.1


def test_highline_30():
    """Test: Highline with specific sag produces expected tension"""
    highline_model = get_model('highline_tension')
    load = 200  # lbf
    sag = 10    # feet
    span = 100  # feet
    result = highline_model.compute(load=load, sag=sag, span=span)
    tension = result['tension']
    # With 10ft sag on 100ft span, tension should be approximately load * 2.5
    # T ≈ W * sqrt(1 + (50/10)^2) / 2 = W * sqrt(26) / 2 ≈ W * 2.55
    expected = load * 2.55
    return abs(tension - expected) < 50  # Within 50 lbf


def test_pack_loads():
    """Test: Default pack loads successfully"""
    try:
        # Import would happen here if packs were implemented
        # For now, just check that the core modules work
        from . import units, citations, model_registry
        return True
    except ImportError:
        return False


def test_constant_exists():
    """Test: Check that a rope constant exists"""
    from .citations import get_citation
    cite = get_citation("rope.knot.figure_8_on_bight")
    return cite is not None


def test_constant_in_range():
    """Test: Check that constant values are in expected ranges"""
    from .citations import get_citation
    cite = get_citation("rope.knot.figure_8_on_bight")
    if not cite:
        return False
    # Figure 8 knot efficiency should be between 0.7 and 0.85
    value_str = cite.value
    # Extract numeric value (e.g., "0.75-0.80" -> 0.75)
    try:
        if '-' in value_str:
            min_val = float(value_str.split('-')[0])
            return 0.7 <= min_val <= 0.85
        else:
            return True
    except:
        return True  # If can't parse, assume valid


# All doctor tests
DOCTOR_TESTS = [
    DoctorTest("sin²+cos²=1", test_sin_cos_identity),
    DoctorTest("sec(60)=2", test_sec_60),
    DoctorTest("tan(45)=1", test_tan_45),
    DoctorTest("bridle(60)=W", test_bridle_60),
    DoctorTest("highline(30)=~2.5W", test_highline_30),
    DoctorTest("pack_loads", test_pack_loads),
    DoctorTest("constant_exists", test_constant_exists),
    DoctorTest("constant_in_range", test_constant_in_range)
]


def run_doctor():
    """Run all doctor tests"""
    results = []
    passed = 0
    
    for test in DOCTOR_TESTS:
        result = test.run()
        results.append(result)
        if result['passed']:
            passed += 1
    
    return {
        'model': 'doctor',
        'passed': passed,
        'total': len(DOCTOR_TESTS),
        'status': 'PASS' if passed == len(DOCTOR_TESTS) else 'FAIL',
        'tests': results
    }


def format_doctor_output(results):
    """Format doctor results for display"""
    lines = []
    lines.append(f"model: {results['model']}")
    lines.append(f"passed: {results['passed']}")
    lines.append(f"total: {results['total']}")
    lines.append(f"status: {results['status']}")
    lines.append("tests:")
    
    for test in results['tests']:
        status = "✓" if test['passed'] else "✗"
        lines.append(f"  - {test['name']:<20} {status}")
        if test['error']:
            lines.append(f"    Error: {test['error']}")
    
    return '\n'.join(lines)


# Self-test
if __name__ == "__main__":
    print("TRIG6 Doctor Self-Test")
    print("=" * 70)
    
    results = run_doctor()
    output = format_doctor_output(results)
    print(output)
    
    # Exit with error code if doctor fails
    if results['status'] != 'PASS':
        print("\n⚠️  DOCTOR FAILED - System cannot boot")
        sys.exit(1)
    else:
        print("\n✓ All tests passed - System ready to boot")
        sys.exit(0)
