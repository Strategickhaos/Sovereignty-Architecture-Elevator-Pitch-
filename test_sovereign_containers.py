#!/usr/bin/env python3
"""
Test Suite for Sovereign Container Infrastructure
Validates core components of Phase 1 implementation
"""

import sys
import os
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        import sovereign_runtime
        print("  ✅ sovereign_runtime imported")
        
        import sovereign_image
        print("  ✅ sovereign_image imported")
        
        import sovereign_volumes
        print("  ✅ sovereign_volumes imported")
        
        import sovereign_network
        print("  ✅ sovereign_network imported")
        
        import flamelang_container_compiler
        print("  ✅ flamelang_container_compiler imported")
        
        import sovereign_orchestrator
        print("  ✅ sovereign_orchestrator imported")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_runtime_creation():
    """Test sovereign runtime creation"""
    print("\n🧪 Testing runtime creation...")
    
    try:
        from sovereign_runtime import SovereignContainer, SovereignRuntime
        
        # Create temporary rootfs
        with tempfile.TemporaryDirectory() as tmpdir:
            rootfs = Path(tmpdir) / "rootfs"
            rootfs.mkdir()
            
            # Create container instance with temporary container_dir
            container = SovereignContainer(
                name="test_container",
                rootfs_path=str(rootfs),
                glyph="[001]"
            )
            container.container_dir = Path(tmpdir) / "containers" / "test_container"
            container.container_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"  ✅ Container created: {container.name}")
            print(f"  ✅ Container ID: {container.container_id}")
            print(f"  ✅ Glyph: {container.glyph}")
            
            # Test runtime manager with temporary base_dir
            runtime = SovereignRuntime()
            runtime.base_dir = Path(tmpdir) / "sovereign"
            runtime.base_dir.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Runtime manager created")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Runtime creation failed: {e}")
        return False


def test_volume_management():
    """Test volume management"""
    print("\n🧪 Testing volume management...")
    
    try:
        from sovereign_volumes import SovereignVolume
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Override volume path for testing
            test_volume_path = Path(tmpdir) / "test_volume"
            test_volume_path.mkdir(parents=True)
            
            volume = SovereignVolume("test_volume")
            volume.volume_path = test_volume_path
            
            # Test file operations
            volume.write_file("test.txt", "Test content")
            content = volume.read_file("test.txt")
            
            assert content == "Test content", "File content mismatch"
            
            print(f"  ✅ Volume created: {volume.name}")
            print(f"  ✅ File write/read successful")
            print(f"  ✅ Volume metadata: {volume.metadata()}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Volume management failed: {e}")
        return False


def test_image_creation():
    """Test image format"""
    print("\n🧪 Testing image creation...")
    
    try:
        from sovereign_image import SovereignImage
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Override image path for testing
            image = SovereignImage("test-image", "latest")
            image.image_dir = Path(tmpdir) / "images"
            image.image_dir.mkdir(parents=True)
            
            # Test Dockerfile parsing
            dockerfile_content = """
FROM alpine:latest
RUN mkdir -p /app
COPY . /app
CMD ["sh"]
"""
            layers = image.parse_dockerfile(dockerfile_content)
            
            print(f"  ✅ Image created: {image.name}:{image.tag}")
            print(f"  ✅ Parsed {len(layers)} layers")
            
            for layer in layers:
                print(f"    - {layer['instruction']} {layer['args'][:50]}")
                
        return True
        
    except Exception as e:
        print(f"  ❌ Image creation failed: {e}")
        return False


def test_flamelang_compiler():
    """Test FlameLang compiler"""
    print("\n🧪 Testing FlameLang compiler...")
    
    try:
        from flamelang_container_compiler import FlameLangContainerCompiler, GlyphTable
        
        # Test glyph table
        glyphs = GlyphTable.list_glyphs()
        print(f"  ✅ Loaded {len(glyphs)} glyphs")
        
        # Test glyph lookup
        aether = GlyphTable.get_glyph("[001]")
        print(f"  ✅ Aether Prime: {aether['frequency']}")
        
        # Create compiler
        compiler = FlameLangContainerCompiler()
        
        # Test manifest parsing
        manifest = """
container TestContainer {
    glyph: [001]
    image: "alpine:latest"
    
    resources: {
        memory: 512M
        cpu: 1
    }
}

network test_net {
    glyph: [200]
    type: "bridge"
    subnet: "10.137.0.0/16"
}

deploy [001]
"""
        
        parsed = compiler.parse_flamelang(manifest)
        
        print(f"  ✅ Parsed manifest:")
        print(f"    - Containers: {len(parsed['containers'])}")
        print(f"    - Networks: {len(parsed['networks'])}")
        print(f"    - Deployment: {parsed['deployment']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ FlameLang compiler failed: {e}")
        return False


def test_orchestrator():
    """Test orchestrator"""
    print("\n🧪 Testing orchestrator...")
    
    try:
        from sovereign_orchestrator import SovereignOrchestrator, SovereignCluster
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Override state directory
            orchestrator = SovereignOrchestrator()
            orchestrator.state_dir = Path(tmpdir) / "orchestrator"
            orchestrator.state_dir.mkdir(parents=True)
            
            # Register test node
            node_spec = {
                'hostname': 'test-node',
                'glyph': '[001]',
                'resources': {'cpu': 4, 'memory_gb': 16}
            }
            
            orchestrator.register_node('node-1', node_spec)
            
            nodes = orchestrator.list_nodes()
            
            print(f"  ✅ Orchestrator created")
            print(f"  ✅ Registered {len(nodes)} node(s)")
            print(f"  ✅ Node authority: {nodes[0]['authority']}")
            
            # Test cluster
            cluster = SovereignCluster()
            cluster.orchestrator = orchestrator
            
            status = cluster.status()
            print(f"  ✅ Cluster status: {status}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Orchestrator failed: {e}")
        return False


def test_network_creation():
    """Test network creation (metadata only, no actual bridge)"""
    print("\n🧪 Testing network metadata...")
    
    try:
        from sovereign_network import SovereignNetwork
        
        with tempfile.TemporaryDirectory() as tmpdir:
            network = SovereignNetwork("test_network", "10.137.0.0/16")
            network.network_dir = Path(tmpdir) / "network"
            network.network_dir.mkdir(parents=True)
            
            # Test IP allocation
            ip = network._allocate_ip("test_container_123")
            
            print(f"  ✅ Network created: {network.name}")
            print(f"  ✅ Bridge: {network.bridge}")
            print(f"  ✅ Subnet: {network.subnet}")
            print(f"  ✅ Allocated IP: {ip}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Network creation failed: {e}")
        return False


def run_all_tests():
    """Run all test suites"""
    print("🔥 Sovereign Container Infrastructure - Test Suite ⚔️🖤\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Runtime Creation", test_runtime_creation),
        ("Volume Management", test_volume_management),
        ("Image Creation", test_image_creation),
        ("FlameLang Compiler", test_flamelang_compiler),
        ("Orchestrator", test_orchestrator),
        ("Network Metadata", test_network_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print("="*60)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🔥 ALL TESTS PASSED! ⚔️🖤")
        print("Sovereign Container Infrastructure is ready!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
