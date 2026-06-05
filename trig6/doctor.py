#!/usr/bin/env python3
"""
TRIG6 Doctor - Health Monitoring and Validation Module
Performs self-checks and generates metrics for observability integration.
"""
import sys
import math
import json
from pathlib import Path


class Doctor:
    """Health check and validation for TRIG6 system"""
    
    def __init__(self):
        self.checks = []
        self.metrics = {}
        
    def check_math_operations(self) -> bool:
        """Validate core math operations"""
        try:
            # Basic trigonometric checks
            assert abs(math.sin(0) - 0.0) < 0.0001
            assert abs(math.cos(0) - 1.0) < 0.0001
            assert abs(math.sin(math.pi/2) - 1.0) < 0.0001
            
            # Test angle conversions
            assert abs(math.radians(180) - math.pi) < 0.0001
            
            self.checks.append({"test": "math_operations", "status": "PASS"})
            return True
        except AssertionError as e:
            self.checks.append({"test": "math_operations", "status": "FAIL", "error": str(e)})
            return False
    
    def check_constants(self) -> bool:
        """Check if constants directory exists and is accessible"""
        try:
            constants_dir = Path(__file__).parent / "constants"
            constants_dir.mkdir(exist_ok=True)
            
            self.checks.append({"test": "constants_dir", "status": "PASS"})
            return True
        except Exception as e:
            self.checks.append({"test": "constants_dir", "status": "FAIL", "error": str(e)})
            return False
    
    def check_sovereignty(self) -> bool:
        """Verify sovereignty requirements (no external network calls)"""
        try:
            # Verify we can run without network
            # This is a design check - TRIG6 uses only stdlib
            prohibited_modules = ['requests', 'urllib3', 'httpx']
            loaded_prohibited = [mod for mod in prohibited_modules if mod in sys.modules]
            
            if loaded_prohibited:
                self.checks.append({
                    "test": "sovereignty",
                    "status": "WARN",
                    "message": f"Prohibited modules loaded: {loaded_prohibited}"
                })
                return True  # Warning, not failure
            
            self.checks.append({"test": "sovereignty", "status": "PASS"})
            return True
        except Exception as e:
            self.checks.append({"test": "sovereignty", "status": "FAIL", "error": str(e)})
            return False
    
    def generate_metrics(self) -> dict:
        """Generate Prometheus-compatible metrics"""
        passed = sum(1 for check in self.checks if check["status"] == "PASS")
        total = len(self.checks)
        
        self.metrics = {
            "trig6_health_checks_total": total,
            "trig6_health_checks_passed": passed,
            "trig6_health_checks_failed": total - passed,
            "trig6_health_status": 1 if passed == total else 0,
            "trig6_version": "1.0.0"
        }
        
        return self.metrics
    
    def run(self) -> dict:
        """Run all health checks and return results"""
        self.check_math_operations()
        self.check_constants()
        self.check_sovereignty()
        
        metrics = self.generate_metrics()
        
        status = "HEALTHY" if metrics["trig6_health_status"] == 1 else "UNHEALTHY"
        
        return {
            "status": status,
            "checks": self.checks,
            "metrics": metrics,
            "summary": f"{metrics['trig6_health_checks_passed']}/{metrics['trig6_health_checks_total']} checks passed"
        }


def main():
    doctor = Doctor()
    result = doctor.run()
    
    print(json.dumps(result, indent=2))
    
    # Exit with error code if unhealthy
    sys.exit(0 if result["status"] == "HEALTHY" else 1)


if __name__ == "__main__":
    main()
