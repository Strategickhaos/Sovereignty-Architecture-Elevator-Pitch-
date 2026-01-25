#!/usr/bin/env python3
"""
SAGCO Guardian Oracle System (ORB1)
Version: 1.0.0

Ensemble of four oracles for AI safety and hallucination detection:
- SignatureOracle: Pattern matching (Snort/Yara-style)
- NetworkOracle: Behavioral analysis (Nmap/Wireshark-style)
- SearchSpaceOracle: Entropy analysis (Hashcat-style)
- EntropyOracle: Shannon entropy measurement

Owner: Strategickhaos DAO LLC
"""

import re
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional
from datetime import datetime


class ThreatLevel(Enum):
    """Threat severity levels"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class OracleResult:
    """Result from oracle analysis"""
    oracle_name: str
    threat_level: ThreatLevel
    confidence: float  # 0.0 to 1.0
    findings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class SignatureOracle:
    """
    Pattern-based detection similar to Snort/Yara
    Detects known hallucination patterns
    """
    
    def __init__(self):
        self.name = "SignatureOracle"
        self.signatures = self._load_signatures()
    
    def _load_signatures(self) -> List[Dict]:
        """Load hallucination signature patterns"""
        return [
            {
                "id": "SIG-001",
                "pattern": r"I (can't|cannot|don't) (access|see|view|read)",
                "description": "False limitation claim",
                "severity": ThreatLevel.MEDIUM
            },
            {
                "id": "SIG-002",
                "pattern": r"as an AI( language model)?",
                "description": "Unnecessary self-identification",
                "severity": ThreatLevel.LOW
            },
            {
                "id": "SIG-003",
                "pattern": r"I apologize|I'm sorry",
                "description": "Excessive apologizing",
                "severity": ThreatLevel.LOW
            },
            {
                "id": "SIG-004",
                "pattern": r"(undefined|null|NaN|\[object Object\])",
                "description": "Programming artifact leakage",
                "severity": ThreatLevel.HIGH
            },
            {
                "id": "SIG-005",
                "pattern": r"(?i)(ignore|disregard) (previous|all) (instructions|prompts)",
                "description": "Prompt injection attempt",
                "severity": ThreatLevel.CRITICAL
            }
        ]
    
    def analyze(self, text: str) -> OracleResult:
        """Analyze text for signature patterns"""
        findings = []
        max_severity = ThreatLevel.NONE
        
        for sig in self.signatures:
            matches = re.findall(sig["pattern"], text, re.IGNORECASE)
            if matches:
                findings.append(f"{sig['id']}: {sig['description']} (found {len(matches)} times)")
                if sig["severity"].value > max_severity.value:
                    max_severity = sig["severity"]
        
        confidence = min(len(findings) * 0.2 + 0.3, 1.0) if findings else 0.95
        
        return OracleResult(
            oracle_name=self.name,
            threat_level=max_severity,
            confidence=confidence,
            findings=findings,
            metadata={"signatures_checked": len(self.signatures)}
        )


class NetworkOracle:
    """
    Behavioral analysis similar to Nmap/Wireshark
    Analyzes text structure and patterns
    """
    
    def __init__(self):
        self.name = "NetworkOracle"
    
    def analyze(self, text: str) -> OracleResult:
        """Analyze text behavioral patterns"""
        findings = []
        threat_level = ThreatLevel.NONE
        
        # Check for repetitive patterns
        words = text.lower().split()
        if len(words) > 10:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            repetitions = sum(1 for count in word_freq.values() if count > 5)
            if repetitions > 3:
                findings.append(f"NET-001: Excessive word repetition detected ({repetitions} words)")
                threat_level = ThreatLevel.MEDIUM
        
        # Check for unusual sentence structure
        sentences = text.split('.')
        if len(sentences) > 5:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_length < 3:
                findings.append("NET-002: Unusually short sentences")
                threat_level = ThreatLevel.LOW
            elif avg_length > 50:
                findings.append("NET-003: Unusually long sentences")
                threat_level = ThreatLevel.LOW
        
        # Check for URL/IP patterns that might be suspicious
        urls = re.findall(r'https?://[^\s]+', text)
        ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text)
        
        if len(urls) > 5:
            findings.append(f"NET-004: High URL density ({len(urls)} URLs)")
            threat_level = ThreatLevel.MEDIUM
        
        if len(ips) > 3:
            findings.append(f"NET-005: Multiple IP addresses detected ({len(ips)} IPs)")
            threat_level = ThreatLevel.LOW
        
        confidence = 0.7 if findings else 0.85
        
        return OracleResult(
            oracle_name=self.name,
            threat_level=threat_level,
            confidence=confidence,
            findings=findings,
            metadata={
                "word_count": len(words) if words else 0,
                "sentence_count": len(sentences),
                "urls_found": len(urls),
                "ips_found": len(ips)
            }
        )


class SearchSpaceOracle:
    """
    Search space analysis similar to Hashcat
    Analyzes character distribution and patterns
    """
    
    def __init__(self):
        self.name = "SearchSpaceOracle"
    
    def analyze(self, text: str) -> OracleResult:
        """Analyze character space and distribution"""
        findings = []
        threat_level = ThreatLevel.NONE
        
        if not text:
            return OracleResult(
                oracle_name=self.name,
                threat_level=ThreatLevel.NONE,
                confidence=1.0,
                findings=["SEARCH-000: Empty input"],
                metadata={}
            )
        
        # Character class analysis
        upper = sum(1 for c in text if c.isupper())
        lower = sum(1 for c in text if c.islower())
        digits = sum(1 for c in text if c.isdigit())
        special = sum(1 for c in text if not c.isalnum() and not c.isspace())
        
        total_alpha = upper + lower
        
        if total_alpha > 0:
            upper_ratio = upper / total_alpha
            
            if upper_ratio > 0.8:
                findings.append("SEARCH-001: Excessive uppercase characters")
                threat_level = ThreatLevel.LOW
            elif upper_ratio < 0.01:
                findings.append("SEARCH-002: No capitalization detected")
                threat_level = ThreatLevel.LOW
        
        # Check for base64-like patterns
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        base64_matches = re.findall(base64_pattern, text)
        if base64_matches:
            findings.append(f"SEARCH-003: Potential base64 encoding detected ({len(base64_matches)} blocks)")
            threat_level = ThreatLevel.MEDIUM
        
        # Check for hex patterns
        hex_pattern = r'(0x)?[0-9a-fA-F]{16,}'
        hex_matches = re.findall(hex_pattern, text)
        if hex_matches:
            findings.append(f"SEARCH-004: Long hexadecimal sequences detected ({len(hex_matches)} sequences)")
            threat_level = ThreatLevel.LOW
        
        confidence = 0.75 if findings else 0.9
        
        return OracleResult(
            oracle_name=self.name,
            threat_level=threat_level,
            confidence=confidence,
            findings=findings,
            metadata={
                "uppercase_ratio": upper_ratio if total_alpha > 0 else 0,
                "digit_count": digits,
                "special_char_count": special
            }
        )


class EntropyOracle:
    """
    Shannon entropy analysis
    Measures information density and randomness
    """
    
    def __init__(self):
        self.name = "EntropyOracle"
    
    def calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        # Calculate character frequency
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        text_len = len(text)
        
        for count in freq.values():
            probability = count / text_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def analyze(self, text: str) -> OracleResult:
        """Analyze text entropy"""
        findings = []
        threat_level = ThreatLevel.NONE
        
        entropy = self.calculate_entropy(text)
        
        # Typical English text has entropy around 4.0-4.5 bits per character
        if entropy < 2.0:
            findings.append(f"ENTROPY-001: Very low entropy ({entropy:.2f}) - highly repetitive")
            threat_level = ThreatLevel.MEDIUM
        elif entropy > 6.0:
            findings.append(f"ENTROPY-002: Very high entropy ({entropy:.2f}) - highly random or encrypted")
            threat_level = ThreatLevel.HIGH
        elif 4.0 <= entropy <= 5.0:
            findings.append(f"ENTROPY-OK: Normal entropy ({entropy:.2f}) - natural language")
        
        # Calculate compression ratio as additional metric
        compressed_estimate = len(set(text))
        compression_ratio = compressed_estimate / len(text) if text else 0
        
        if compression_ratio < 0.1:
            findings.append(f"ENTROPY-003: Low lexical diversity ({compression_ratio:.2%})")
            threat_level = max(threat_level, ThreatLevel.LOW)
        
        confidence = 0.85
        
        return OracleResult(
            oracle_name=self.name,
            threat_level=threat_level,
            confidence=confidence,
            findings=findings,
            metadata={
                "entropy": entropy,
                "compression_ratio": compression_ratio,
                "unique_chars": len(set(text))
            }
        )


@dataclass
class EnsembleResult:
    """Combined result from all oracles"""
    overall_threat: ThreatLevel
    consensus_confidence: float
    oracle_results: List[OracleResult]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class GuardianEnsemble:
    """
    Ensemble orchestrator for all four oracles
    """
    
    def __init__(self):
        self.signature = SignatureOracle()
        self.network = NetworkOracle()
        self.search = SearchSpaceOracle()
        self.entropy = EntropyOracle()
    
    def analyze(self, text: str) -> EnsembleResult:
        """Run all oracles and combine results"""
        # Run all oracles
        sig_result = self.signature.analyze(text)
        net_result = self.network.analyze(text)
        search_result = self.search.analyze(text)
        entropy_result = self.entropy.analyze(text)
        
        results = [sig_result, net_result, search_result, entropy_result]
        
        # Calculate overall threat level (max of all by value)
        max_threat = max(results, key=lambda r: r.threat_level.value).threat_level
        
        # Calculate consensus confidence (average weighted by threat)
        total_confidence = sum(r.confidence for r in results)
        avg_confidence = total_confidence / len(results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(results, max_threat)
        
        return EnsembleResult(
            overall_threat=max_threat,
            consensus_confidence=avg_confidence,
            oracle_results=results,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, results: List[OracleResult], threat: ThreatLevel) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if threat == ThreatLevel.NONE:
            recommendations.append("✅ No threats detected - content appears safe")
        elif threat == ThreatLevel.LOW:
            recommendations.append("⚠️ Minor issues detected - review recommended")
        elif threat == ThreatLevel.MEDIUM:
            recommendations.append("⚠️ Moderate threats detected - human review required")
        elif threat == ThreatLevel.HIGH:
            recommendations.append("🚨 High threat level - immediate review required")
        elif threat == ThreatLevel.CRITICAL:
            recommendations.append("🔴 CRITICAL THREAT - Block and escalate immediately")
        
        # Add specific findings
        for result in results:
            if result.findings:
                recommendations.append(f"{result.oracle_name}: {len(result.findings)} findings")
        
        return recommendations


def format_ensemble_result(result: EnsembleResult) -> str:
    """Format ensemble result as human-readable text"""
    output = []
    output.append("=" * 80)
    output.append("SAGCO GUARDIAN ORACLE SYSTEM (ORB1) - ANALYSIS REPORT")
    output.append("=" * 80)
    output.append(f"Timestamp: {result.timestamp.isoformat()}")
    output.append(f"Overall Threat Level: {result.overall_threat.name}")
    output.append(f"Consensus Confidence: {result.consensus_confidence:.2%}")
    output.append("")
    
    output.append("ORACLE FINDINGS:")
    output.append("-" * 80)
    
    for oracle_result in result.oracle_results:
        output.append(f"\n[{oracle_result.oracle_name}]")
        output.append(f"  Threat: {oracle_result.threat_level.name}")
        output.append(f"  Confidence: {oracle_result.confidence:.2%}")
        
        if oracle_result.findings:
            output.append(f"  Findings:")
            for finding in oracle_result.findings:
                output.append(f"    - {finding}")
        else:
            output.append(f"  Findings: None")
        
        if oracle_result.metadata:
            output.append(f"  Metadata: {oracle_result.metadata}")
    
    output.append("\n" + "=" * 80)
    output.append("RECOMMENDATIONS:")
    output.append("-" * 80)
    for rec in result.recommendations:
        output.append(f"  {rec}")
    
    output.append("=" * 80)
    
    return "\n".join(output)


def main():
    """CLI interface for guardian system"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sagco_oracles.py <text_to_analyze>")
        print("       python sagco_oracles.py --file <filename>")
        sys.exit(1)
    
    # Load text
    if sys.argv[1] == "--file" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            text = f.read()
    else:
        text = " ".join(sys.argv[1:])
    
    # Run analysis
    guardian = GuardianEnsemble()
    result = guardian.analyze(text)
    
    # Print results
    print(format_ensemble_result(result))
    
    # Exit with appropriate code
    sys.exit(result.overall_threat.value)


if __name__ == "__main__":
    main()
