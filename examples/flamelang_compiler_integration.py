#!/usr/bin/env python3
"""
Example: FlameLang Compiler Integration with System Health Controller

This demonstrates how to integrate the System Health Controller
with a compiler to adapt behavior based on system health.
"""

import sys
import time
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.system_health import SystemHealthController


class FlameLangCompiler:
    """
    Mock FlameLang compiler that adapts to system health
    """
    
    def __init__(self, health_controller: SystemHealthController):
        self.health = health_controller
        self.compiled_files = []
        
    def compile_project(self, project_path: str) -> bool:
        """
        Compile a project with health-aware settings
        
        Args:
            project_path: Path to project
        
        Returns:
            True if compilation succeeded
        """
        # Log compilation start
        self.health.log_compile_event('start', {
            'target': project_path,
            'pid': os.getpid()
        })
        
        # Get compiler configuration based on current health
        config = self.health.get_compiler_config()
        
        print(f"\n🔨 Compiling: {project_path}")
        print(f"   Mode: {config['mode']}")
        print(f"   Optimization level: {config['opt_level']}")
        print(f"   Parallel jobs: {config['parallel_jobs']:.0f}")
        print(f"   Proof threshold: {config['proof_threshold']:.2f}")
        
        # Simulate compilation based on config
        try:
            if config['mode'] == 'FULL':
                # Full power compilation
                print("   ⚡ Running aggressive optimizations...")
                if config.get('enable_lto'):
                    print("   🔗 Link-time optimization enabled")
                if config.get('aggressive_inlining'):
                    print("   📈 Aggressive inlining enabled")
                time.sleep(0.5)
                
            elif config['mode'] == 'DEGRADED':
                # Conservative compilation
                print("   ⚠️  Running conservative optimizations...")
                print("   🛡️  Reducing memory footprint")
                time.sleep(0.3)
                
            else:  # SAFE
                # Minimal compilation with safety checks
                print("   🔒 Running minimal optimizations...")
                print("   ✅ Extra safety checks enabled")
                if config.get('enable_safety_checks'):
                    print("   🔍 Validating all intermediate steps")
                time.sleep(0.2)
            
            # Simulate proof checking
            if self._check_proofs(config['proof_threshold']):
                print("   ✅ All proofs validated")
                success = True
            else:
                print("   ❌ Proof validation failed")
                success = False
            
            # Log completion
            self.health.log_compile_event('end', {
                'target': project_path,
                'success': success,
                'duration_sec': 0.5
            })
            
            if success:
                self.compiled_files.append(project_path)
                print(f"   ✅ Compilation succeeded")
            
            return success
            
        except Exception as e:
            print(f"   ❌ Compilation failed: {e}")
            self.health.log_compile_event('error', {
                'target': project_path,
                'error': str(e)
            })
            return False
    
    def _check_proofs(self, threshold: float) -> bool:
        """
        Validate proofs with specified rigor threshold
        
        Args:
            threshold: Rigor level [0, 1]
        
        Returns:
            True if proofs pass
        """
        if threshold > 0.8:
            # Maximum rigor: full validation
            print("   🔬 Running full proof validation (strict mode)")
            time.sleep(0.2)
            return True
        elif threshold > 0.5:
            # Moderate rigor: standard validation
            print("   🔬 Running standard proof validation")
            time.sleep(0.1)
            return True
        else:
            # Low rigor: fast validation
            print("   🔬 Running fast proof validation")
            time.sleep(0.05)
            return True


def main():
    """Example integration workflow"""
    
    print("=" * 70)
    print("  FlameLang Compiler with System Health Integration")
    print("=" * 70)
    
    # Initialize health controller
    print("\n🚀 Initializing System Health Controller...")
    controller = SystemHealthController(log_dir="./logs/flamelang_demo")
    controller.initialize()
    
    # Create compiler with health awareness
    compiler = FlameLangCompiler(controller)
    
    # Compile some projects
    projects = [
        "myproject/core",
        "myproject/stdlib",
        "myproject/runtime"
    ]
    
    print("\n" + "=" * 70)
    print("  Compilation Workflow")
    print("=" * 70)
    
    for project in projects:
        # Get current system status
        status = controller.get_system_status()
        
        print(f"\n📊 System Status:")
        print(f"   Health: f={status['health']['f']:.3f}")
        print(f"   Mode: {status['health']['mode']}")
        print(f"   Uptime: {status['uptime_seconds']:.1f}s")
        if status['stability_rate']:
            print(f"   Stability: Γ={status['stability_rate']:.4f}")
        
        print(f"\n📜 System Contract:")
        print(f"   {status['contract']}")
        
        # Compile
        success = compiler.compile_project(project)
        
        if not success:
            print(f"\n⚠️  Compilation failed, system may be under stress")
            print("   Consider:")
            print("   - Reducing parallel jobs")
            print("   - Lowering optimization level")
            print("   - Waiting for system to stabilize")
        
        # Brief pause between compilations
        time.sleep(0.5)
    
    # Final status
    print("\n" + "=" * 70)
    print("  Final Status")
    print("=" * 70)
    
    status = controller.get_system_status()
    print(f"\n✅ Compiled {len(compiler.compiled_files)} projects successfully")
    print(f"   Final health: f={status['health']['f']:.3f}")
    print(f"   Total ticks: {status['tick_count']}")
    print(f"   Logs written to: {controller.log_dir}")
    
    # Show log files
    print(f"\n📁 Log files created:")
    for logfile in sorted(controller.log_dir.glob("*")):
        print(f"   - {logfile.name}")
    
    print("\n" + "=" * 70)
    print("  Demo Complete")
    print("=" * 70)
    print("\n📝 This demonstrates:")
    print("   - Health-aware compilation")
    print("   - Adaptive optimization levels")
    print("   - Proof rigor based on system state")
    print("   - Comprehensive logging")
    print("\n🎯 The compiler now has a contract with the system:")
    print('   "When my health falls, I narrow my blast radius."')
    print()


if __name__ == "__main__":
    main()
