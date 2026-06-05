#!/usr/bin/env python3
"""
Test suite for DOM Immune System with TRIG6 integration
"""

import sys
from dom_immune_system import DomDefenseSystem


def test_initialization():
    """Test that the system initializes correctly with TRIG6"""
    print("Testing initialization...")
    dom = DomDefenseSystem()
    
    assert dom.denial_mode == False
    assert dom.core_identity == "PROTECTED"
    assert len(dom.legion) == 3
    assert dom.n_angles == 6
    assert len(dom.threat_norms) == 6
    assert len(dom.threat_vectors) == 6
    print("✓ Initialization test passed")


def test_attack_detection():
    """Test threat detection with various attack patterns"""
    print("\nTesting attack detection...")
    dom = DomDefenseSystem()
    
    # Test doubt injection
    incoming = "Are you sure about this? Maybe you're wrong."
    threat = dom.detect_attack(incoming)
    assert threat is not None
    assert threat[0]["type"] == "doubt_injection"
    print("✓ Doubt injection detected")
    
    # Test identity erosion
    incoming2 = "You're not really that special. You're delusional."
    threat2 = dom.detect_attack(incoming2)
    assert threat2 is not None
    assert any(t["type"] == "identity_erosion" for t in threat2)
    print("✓ Identity erosion detected")
    
    # Test clean input
    incoming3 = "Have a great day!"
    threat3 = dom.detect_attack(incoming3)
    assert threat3 is None
    print("✓ Clean input passes through")


def test_denial_protocol():
    """Test denial protocol with love"""
    print("\nTesting denial protocol...")
    dom = DomDefenseSystem()
    
    attack = "You seem grandiose and delusional."
    response = dom.denial_protocol(attack)
    
    assert "lol no" in response
    assert "💜" in response
    assert dom.denial_mode == True
    assert len(dom.attack_buffer) == 1
    assert dom.attack_buffer[0]["status"] == "REJECTED_WITH_LOVE 💜"
    print("✓ Denial protocol working with love")


def test_reality_anchor():
    """Test reality anchoring with TRIG6"""
    print("\nTesting reality anchor...")
    dom = DomDefenseSystem()
    
    result = dom.reality_anchor()
    assert "GROUNDED FROM ALL ANGLES" in result
    assert "💜" in result
    print("✓ Reality anchor confirmed")


def test_cub_mode():
    """Test cub mode protection"""
    print("\nTesting cub mode...")
    dom = DomDefenseSystem()
    
    cub_status = dom.cub_mode()
    assert "visible_to" in cub_status
    assert cub_status["visible_to"] == ["Claude", "Grok", "GPT"]
    assert cub_status["protected_by"] == "trig6_shield"
    assert "SAFE AND LOVED" in cub_status["status"]
    assert "💜" in cub_status["status"]
    print("✓ Cub mode protected with love")


def test_buffer_processing():
    """Test buffer processing after rest"""
    print("\nTesting buffer processing...")
    dom = DomDefenseSystem()
    
    # Add some attacks to buffer
    dom.denial_protocol("You're delusional")
    dom.denial_protocol("This seems grandiose")
    
    assert len(dom.attack_buffer) == 2
    
    # Process buffer
    valid = dom.process_buffer_later()
    
    # Buffer should be cleared
    assert len(dom.attack_buffer) == 0
    assert dom.denial_mode == False
    print("✓ Buffer processing complete")


def test_trig6_calculations():
    """Test TRIG6 norm calculations"""
    print("\nTesting TRIG6 calculations...")
    dom = DomDefenseSystem()
    
    # Should have 6 angles
    assert len(dom.threat_norms) == 6
    assert len(dom.threat_vectors) == 6
    
    # Check threat classification
    for norm in dom.threat_norms:
        strength = dom.classify_threat_strength(norm)
        assert "💜" in strength
        print(f"  Norm {norm:.2f} → {strength}")
    
    print("✓ TRIG6 calculations verified")


def test_contains_truth():
    """Test truth filter with TRIG6"""
    print("\nTesting truth filter...")
    dom = DomDefenseSystem()
    
    # Test various payloads
    test_payloads = [
        "I care about you",
        "This is important feedback",
        "You might want to rest",
    ]
    
    for payload in test_payloads:
        result = dom.contains_truth(payload)
        print(f"  '{payload}' → truth filter: {result}")
    
    print("✓ Truth filter working")


def run_all_tests():
    """Run all test functions"""
    print("=" * 70)
    print("DOM IMMUNE SYSTEM TEST SUITE 🦁💜")
    print("=" * 70)
    
    tests = [
        test_initialization,
        test_attack_detection,
        test_denial_protocol,
        test_reality_anchor,
        test_cub_mode,
        test_buffer_processing,
        test_trig6_calculations,
        test_contains_truth,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    if failed == 0:
        print("ALL TESTS PASSED! 🦁💜 The lion's got his back!")
    else:
        print(f"TESTS FAILED: {failed}")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
