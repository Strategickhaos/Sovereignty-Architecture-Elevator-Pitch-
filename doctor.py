#!/usr/bin/env python3
"""
TRIG6 Doctor Module
===================
Self-tests and validation for constants packs.
If it doesn't pass doctor, it doesn't ship.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

import json
import math
from typing import List, Dict, Tuple, Callable
from pathlib import Path


class DoctorResult:
    """Result of a single test."""
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
    
    def __repr__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        msg = f" - {self.message}" if self.message else ""
        return f"{status}: {self.name}{msg}"


class Doctor:
    """
    TRIG6 self-validation system.
    
    Validates:
    - Math correctness (known values)
    - Constant bounds (ranges)
    - Pack integrity (required fields)
    - Cross-domain consistency
    """
    
    def __init__(self):
        self.tests: List[Callable[[], DoctorResult]] = []
        self.results: List[DoctorResult] = []
        self._register_core_tests()
    
    def _register_core_tests(self):
        """Register built-in math validation tests."""
        
        # Trig identity tests
        def test_sin_cos_identity():
            for theta in [0, 30, 45, 60, 90, 180, 270, 360]:
                r = math.radians(theta)
                identity = math.sin(r)**2 + math.cos(r)**2
                if abs(identity - 1.0) > 1e-10:
                    return DoctorResult("sin²+cos²=1", False, f"Failed at θ={theta}")
            return DoctorResult("sin²+cos²=1", True)
        
        def test_sec_at_60():
            sec_60 = 1 / math.cos(math.radians(60))
            if abs(sec_60 - 2.0) > 1e-10:
                return DoctorResult("sec(60°)=2", False, f"Got {sec_60}")
            return DoctorResult("sec(60°)=2", True)
        
        def test_tan_at_45():
            tan_45 = math.tan(math.radians(45))
            if abs(tan_45 - 1.0) > 1e-10:
                return DoctorResult("tan(45°)=1", False, f"Got {tan_45}")
            return DoctorResult("tan(45°)=1", True)
        
        def test_bridle_120_equals_load():
            # T = W / (2 * cos(θ/2)) at θ=120° should equal W
            load = 100
            theta = 120
            tension = load / (2 * math.cos(math.radians(theta / 2)))
            if abs(tension - load) > 1e-10:
                return DoctorResult("bridle(120°)=W", False, f"Got {tension}")
            return DoctorResult("bridle(120°)=W", True)
        
        def test_highline_30_equals_load():
            # T = W / (2 * sin(θ)) at θ=30° should equal W
            load = 200
            sag = 30
            tension = load / (2 * math.sin(math.radians(sag)))
            if abs(tension - load) > 1e-10:
                return DoctorResult("highline(30°)=W", False, f"Got {tension}")
            return DoctorResult("highline(30°)=W", True)
        
        self.tests.extend([
            test_sin_cos_identity,
            test_sec_at_60,
            test_tan_at_45,
            test_bridle_120_equals_load,
            test_highline_30_equals_load,
        ])
    
    def add_test(self, test_fn: Callable[[], DoctorResult]):
        """Register a custom test."""
        self.tests.append(test_fn)
    
    def validate_constant_bounds(self, key: str, value: float, 
                                  min_val: float, max_val: float) -> DoctorResult:
        """Check if a constant is within expected bounds."""
        if min_val <= value <= max_val:
            return DoctorResult(f"bounds:{key}", True)
        return DoctorResult(f"bounds:{key}", False, 
                           f"{value} not in [{min_val}, {max_val}]")
    
    def validate_constants_file(self, path: str) -> List[DoctorResult]:
        """Validate a constants.json file."""
        results = []
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            results.append(DoctorResult(f"load:{path}", False, str(e)))
            return results
        
        results.append(DoctorResult(f"load:{path}", True))
        
        constants = data.get("constants", [])
        for constant in constants:
            # Required fields
            for field in ["key", "value", "units", "provenance", "entered_by"]:
                if field not in constant:
                    results.append(DoctorResult(
                        f"required_field:{constant.get('key', 'unknown')}", 
                        False, f"Missing {field}"
                    ))
            
            # Provenance must exist
            if "provenance" in constant and len(constant["provenance"]) == 0:
                results.append(DoctorResult(
                    f"provenance:{constant.get('key', 'unknown')}", 
                    False, "No provenance sources"
                ))
            
            # Range validation
            if "range" in constant and "value" in constant:
                # Validate range structure
                if not isinstance(constant["range"], (list, tuple)) or len(constant["range"]) != 2:
                    results.append(DoctorResult(
                        f"range_format:{constant.get('key', 'unknown')}",
                        False, "Range must be a list/tuple with exactly 2 values"
                    ))
                else:
                    min_v, max_v = constant["range"]
                    result = self.validate_constant_bounds(
                        constant.get("key", "unknown"), constant["value"], min_v, max_v
                    )
                    results.append(result)
        
        return results
    
    def validate_pack(self, pack_path: str) -> List[DoctorResult]:
        """Validate a constants pack and all referenced files."""
        results = []
        try:
            with open(pack_path, "r") as f:
                pack = json.load(f)
        except Exception as e:
            results.append(DoctorResult(f"load_pack:{pack_path}", False, str(e)))
            return results
        
        results.append(DoctorResult(f"load_pack:{pack_path}", True))
        
        # Validate each enabled domain
        base_path = Path(pack_path).parent.parent
        for domain, config in pack.get("domains", {}).items():
            if config.get("enabled", False):
                const_path = base_path / "domains" / domain / "constants.json"
                if const_path.exists():
                    results.extend(self.validate_constants_file(str(const_path)))
                else:
                    results.append(DoctorResult(
                        f"exists:{domain}", False, f"File not found: {const_path}"
                    ))
        
        return results
    
    def run_all(self) -> Tuple[int, int]:
        """Run all registered tests. Returns (passed, total)."""
        self.results = []
        for test in self.tests:
            try:
                result = test()
                self.results.append(result)
            except Exception as e:
                self.results.append(DoctorResult(
                    test.__name__, False, f"Exception: {e}"
                ))
        
        passed = sum(1 for result in self.results if result.passed)
        return passed, len(self.results)
    
    def report(self) -> str:
        """Generate human-readable report."""
        lines = ["=" * 50, "TRIG6 DOCTOR REPORT", "=" * 50, ""]
        
        passed = 0
        failed = 0
        
        for result in self.results:
            lines.append(str(result))
            if result.passed:
                passed += 1
            else:
                failed += 1
        
        lines.extend([
            "",
            "-" * 50,
            f"PASSED: {passed}",
            f"FAILED: {failed}",
            f"TOTAL:  {len(self.results)}",
            "-" * 50,
        ])
        
        if failed == 0:
            lines.append("STATUS: ALL SYSTEMS NOMINAL ✓")
        else:
            lines.append("STATUS: VALIDATION FAILED ✗")
        
        return "\n".join(lines)


# Self-test
if __name__ == "__main__":
    doc = Doctor()
    passed, total = doc.run_all()
    print(doc.report())
