#!/usr/bin/env python3
"""
FlameLang WireGuard DNS - Integration Test Suite
================================================

Comprehensive tests for FlameLang compilation pipeline,
36 tools integration, and DNS security features.

Author: Strategickhaos DAO LLC
Version: 1.0
"""

import sys
import json
import time
from typing import Dict, List, Tuple

# Import FlameLang modules
try:
    from flamelang_wireguard_dns import (
        FlameLangCompiler,
        WireGuardDNSHardener,
        DNSOperation,
        MEROITIC_DNS_GLYPHS
    )
    from flamelang_36_tools_integration import (
        FlameLangToolConverter,
        ADVANCED_TOOLS,
        ToolCategory
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Ensure flamelang_wireguard_dns.py and flamelang_36_tools_integration.py are in the same directory")
    sys.exit(1)


class TestRunner:
    """Test suite runner"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        
    def test(self, name: str, func) -> bool:
        """Run a single test"""
        try:
            print(f"\n  Testing: {name}...", end=" ")
            result = func()
            if result:
                print("✅ PASS")
                self.passed += 1
                self.tests.append((name, True, None))
                return True
            else:
                print("❌ FAIL")
                self.failed += 1
                self.tests.append((name, False, "Test returned False"))
                return False
        except Exception as e:
            print(f"❌ FAIL - {str(e)}")
            self.failed += 1
            self.tests.append((name, False, str(e)))
            return False
    
    def summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        
        if self.failed > 0:
            print("\nFailed Tests:")
            for name, passed, error in self.tests:
                if not passed:
                    print(f"  ❌ {name}")
                    if error:
                        print(f"     Error: {error}")
        
        success_rate = (self.passed / (self.passed + self.failed)) * 100 if (self.passed + self.failed) > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        return self.failed == 0


def test_glyph_mapping():
    """Test that all glyphs are properly defined"""
    assert len(MEROITIC_DNS_GLYPHS) == 23, f"Expected 23 glyphs, got {len(MEROITIC_DNS_GLYPHS)}"
    
    # Check required glyphs
    required = ["tunnel", "query", "resolve", "sovereign", "encrypt"]
    for req in required:
        assert req in MEROITIC_DNS_GLYPHS, f"Missing required glyph: {req}"
    
    # Check glyph structure
    for name, glyph in MEROITIC_DNS_GLYPHS.items():
        assert glyph.symbol, f"Glyph {name} missing symbol"
        assert glyph.frequency > 0, f"Glyph {name} has invalid frequency"
        assert len(glyph.codon_map) == 2, f"Glyph {name} should have 2 codons"
    
    return True


def test_compilation_pipeline():
    """Test FlameLang 5-layer compilation"""
    compiler = FlameLangCompiler()
    
    operation = DNSOperation(
        operation="test_compile",
        params={"test": True},
        entropy_level=0.5,
        trust_score=1.0
    )
    
    compiled = compiler.compile(operation)
    
    # Check all layers exist
    assert "layers" in compiled
    assert "linguistic" in compiled["layers"]
    assert "numeric" in compiled["layers"]
    assert "wave" in compiled["layers"]
    assert "biological" in compiled["layers"]
    assert "machine" in compiled["layers"]
    
    # Check linguistic layer
    linguistic = compiled["layers"]["linguistic"]
    assert len(linguistic) > 0, "Linguistic layer is empty"
    
    # Check numeric layer
    numeric = compiled["layers"]["numeric"]
    assert ":" in numeric, "Numeric layer should contain entropy hash"
    
    # Check wave layer
    wave = compiled["layers"]["wave"]
    assert "frequency" in wave
    assert "amplitude" in wave
    assert "phase" in wave
    assert wave["frequency"] > 0
    
    # Check biological layer
    biological = compiled["layers"]["biological"]
    assert len(biological) > 0, "Biological layer is empty"
    # Should contain only ACGT
    assert all(c in "ACGT" for c in biological), "Biological layer contains non-DNA characters"
    
    # Check machine layer
    machine = compiled["layers"]["machine"]
    assert "define i32" in machine, "Machine layer should contain LLVM IR"
    
    # Check compression ratio
    assert "compression_ratio" in compiled
    assert compiled["compression_ratio"] > 0
    
    return True


def test_dns_leak_detection():
    """Test DNS leak detection algorithm"""
    hardener = WireGuardDNSHardener()
    
    # Test on trusted WireGuard interface
    leak1 = hardener.detect_dns_leak("example.com", "wg0")
    assert not leak1, "Should not detect leak on WireGuard interface"
    
    # Test on untrusted interface with high entropy
    leak2 = hardener.detect_dns_leak("very.long.suspicious.query.example.com", "eth0")
    # May or may not leak depending on entropy calculation
    assert isinstance(leak2, bool), "Should return boolean"
    
    # Test entropy calculation
    entropy1 = hardener._calculate_entropy("simple.com")
    entropy2 = hardener._calculate_entropy("complex.random.entropy.high.example.com")
    assert 0 <= entropy1 <= 1, "Entropy should be 0-1"
    assert 0 <= entropy2 <= 1, "Entropy should be 0-1"
    
    # Test trust calculation
    trust_wg = hardener._calculate_trust("wg0")
    trust_eth = hardener._calculate_trust("eth0")
    assert trust_wg == 1.0, "WireGuard interface should have full trust"
    assert trust_eth < trust_wg, "Ethernet should have lower trust than WireGuard"
    
    return True


def test_dns_poisoning_mitigation():
    """Test DNS poisoning mitigation"""
    hardener = WireGuardDNSHardener()
    
    response = {
        "domain": "test.example.com",
        "ip": "203.0.113.1",
        "ttl": 3600
    }
    
    verified = hardener.mitigate_dns_poisoning(response)
    
    assert "flamelang_signature" in verified, "Should add FlameLang signature"
    assert "verified" in verified, "Should have verified flag"
    assert verified["verified"] == True, "Should be marked as verified"
    assert len(verified["flamelang_signature"]) > 0, "Signature should not be empty"
    
    # Signature should be DNA sequence
    signature = verified["flamelang_signature"]
    assert all(c in "ACGT" for c in signature), "Signature should be DNA sequence"
    
    return True


def test_sovereign_dns_config():
    """Test sovereign DNS configuration generation"""
    hardener = WireGuardDNSHardener()
    
    config = {
        "private_key": "TEST_PRIVATE_KEY",
        "address": "10.99.0.2/24",
        "dns": "10.99.0.1",
        "peer_key": "TEST_PEER_KEY",
        "endpoint": "vpn.test.com:51820",
        "allowed_ips": "0.0.0.0/0"
    }
    
    wg_config = hardener.configure_sovereign_dns(config)
    
    assert "[Interface]" in wg_config, "Should have Interface section"
    assert "[Peer]" in wg_config, "Should have Peer section"
    assert "TEST_PRIVATE_KEY" in wg_config, "Should include private key"
    assert "TEST_PEER_KEY" in wg_config, "Should include peer key"
    assert "FlameLang Sovereign DNS Protection" in wg_config, "Should have FlameLang marker"
    assert "Linguistic:" in wg_config, "Should include linguistic layer"
    assert "Biological:" in wg_config, "Should include biological layer"
    assert "Compression:" in wg_config, "Should include compression ratio"
    
    return True


def test_36_tools_loaded():
    """Test that all 36 tools are loaded"""
    assert len(ADVANCED_TOOLS) == 36, f"Expected 36 tools, got {len(ADVANCED_TOOLS)}"
    
    # Check tool IDs are unique and sequential
    ids = [tool.id for tool in ADVANCED_TOOLS]
    assert ids == list(range(1, 37)), "Tool IDs should be 1-36"
    
    # Check each tool has required fields
    for tool in ADVANCED_TOOLS:
        assert tool.name, f"Tool {tool.id} missing name"
        assert tool.category, f"Tool {tool.id} missing category"
        assert tool.description, f"Tool {tool.id} missing description"
        assert tool.core_functions, f"Tool {tool.id} missing core_functions"
        assert tool.flamelang_layer, f"Tool {tool.id} missing flamelang_layer"
    
    return True


def test_tool_categories():
    """Test tool category distribution"""
    converter = FlameLangToolConverter()
    
    # Count by category
    categories = {}
    for tool in ADVANCED_TOOLS:
        cat = tool.category
        categories[cat] = categories.get(cat, 0) + 1
    
    # Verify we have tools in each major category
    assert ToolCategory.VPN_WIREGUARD in categories, "Missing VPN/WireGuard tools"
    assert ToolCategory.DNS_SECURITY in categories, "Missing DNS security tools"
    assert ToolCategory.C2_PERSISTENCE in categories, "Missing C2 tools"
    
    # Verify category counts make sense
    assert categories[ToolCategory.VPN_WIREGUARD] >= 5, "Should have multiple WireGuard tools"
    assert categories[ToolCategory.DNS_SECURITY] >= 3, "Should have multiple DNS tools"
    
    return True


def test_tool_conversion():
    """Test tool conversion to FlameLang"""
    converter = FlameLangToolConverter()
    
    # Convert a specific tool (Sliver C2)
    sliver = converter.convert_tool(1)
    
    assert sliver["tool_id"] == 1
    assert sliver["tool_name"] == "Sliver C2"
    assert "flamelang_layer" in sliver
    assert "extracted_functions" in sliver
    assert "glyph_mapping" in sliver
    assert "sovereignty_enhancement" in sliver
    assert "deployment" in sliver
    
    # Check extracted functions
    functions = sliver["extracted_functions"]
    assert len(functions) > 0, "Should have extracted functions"
    for func in functions:
        assert "function_name" in func
        assert "layer" in func
        assert "dns_relevance" in func
    
    # Check deployment config
    deployment = sliver["deployment"]
    assert "container_image" in deployment
    assert "dns_protection" in deployment
    assert deployment["dns_protection"] == True
    
    return True


def test_tool_manifest_generation():
    """Test integration manifest generation"""
    converter = FlameLangToolConverter()
    
    manifest = converter.generate_integration_manifest()
    
    assert "version" in manifest
    assert "total_tools" in manifest
    assert "categories" in manifest
    assert "tools" in manifest
    
    assert manifest["total_tools"] == 36
    assert len(manifest["tools"]) == 36
    assert len(manifest["categories"]) > 0
    
    # Verify manifest structure
    for tool_data in manifest["tools"]:
        assert "tool_id" in tool_data
        assert "tool_name" in tool_data
        assert "flamelang_layer" in tool_data
    
    return True


def test_tools_by_layer():
    """Test getting tools by FlameLang layer"""
    converter = FlameLangToolConverter()
    
    # Test each layer
    layers = ["linguistic", "numeric", "wave", "biological", "machine"]
    
    for layer in layers:
        tools = converter.get_tools_by_layer(layer)
        assert len(tools) > 0, f"Should have tools in {layer} layer"
        
        # Verify all tools are in correct layer
        for tool in tools:
            assert tool.flamelang_layer == layer
    
    return True


def test_performance_benchmark():
    """Test compilation performance"""
    compiler = FlameLangCompiler()
    iterations = 100
    
    start = time.time()
    for i in range(iterations):
        operation = DNSOperation(
            operation=f"benchmark_{i}",
            params={"index": i},
            entropy_level=0.5,
            trust_score=1.0
        )
        compiler.compile(operation)
    end = time.time()
    
    avg_time = (end - start) / iterations
    
    # Should complete reasonably fast (< 50ms per operation)
    assert avg_time < 0.05, f"Compilation too slow: {avg_time*1000:.2f}ms per operation"
    
    print(f" ({avg_time*1000:.2f}ms avg)", end="")
    
    return True


def main():
    """Run all tests"""
    print("🔥 FlameLang WireGuard DNS - Integration Test Suite")
    print("="*60)
    
    runner = TestRunner()
    
    print("\n📋 Core FlameLang Tests:")
    runner.test("Glyph Mapping", test_glyph_mapping)
    runner.test("Compilation Pipeline", test_compilation_pipeline)
    runner.test("Performance Benchmark", test_performance_benchmark)
    
    print("\n🔒 DNS Security Tests:")
    runner.test("DNS Leak Detection", test_dns_leak_detection)
    runner.test("DNS Poisoning Mitigation", test_dns_poisoning_mitigation)
    runner.test("Sovereign DNS Config", test_sovereign_dns_config)
    
    print("\n🛠️  Tool Integration Tests:")
    runner.test("36 Tools Loaded", test_36_tools_loaded)
    runner.test("Tool Categories", test_tool_categories)
    runner.test("Tool Conversion", test_tool_conversion)
    runner.test("Manifest Generation", test_tool_manifest_generation)
    runner.test("Tools by Layer", test_tools_by_layer)
    
    # Print summary
    success = runner.summary()
    
    if success:
        print("\n✅ All tests passed! FlameLang implementation is ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
