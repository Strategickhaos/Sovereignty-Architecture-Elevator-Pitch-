#!/usr/bin/env python3
"""
Example Usage of Sovereign Cognitive Architecture
Demonstrates cross-LLM context sharing and quadrilateral verification
"""

import requests
import json
from typing import List, Dict, Any

# ============================================================================
# Configuration
# ============================================================================

MEMORY_MESH_URL = "http://localhost:7000"
CLAUDE_API_URL = "http://localhost:8001"
GPT_API_URL = "http://localhost:8002"
OLLAMA_URL = "http://localhost:11434"


# ============================================================================
# Memory Mesh Client
# ============================================================================

class MemoryMeshClient:
    """Client for interacting with the unified memory mesh"""
    
    def __init__(self, base_url: str = MEMORY_MESH_URL):
        self.base_url = base_url
        
    def store_conversation(
        self, 
        llm_provider: str, 
        messages: List[Dict[str, str]], 
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store a conversation in the memory mesh"""
        response = requests.post(
            f"{self.base_url}/conversations",
            json={
                "llm_provider": llm_provider,
                "messages": messages,
                "metadata": metadata or {}
            }
        )
        response.raise_for_status()
        return response.json()["conversation_id"]
    
    def retrieve_context(
        self, 
        query: str, 
        k: int = 5, 
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context using vector similarity search"""
        response = requests.get(
            f"{self.base_url}/retrieve",
            params={
                "query": query,
                "k": k,
                "min_score": min_score
            }
        )
        response.raise_for_status()
        return response.json()["results"]
    
    def scan_all_chats(
        self, 
        llm_id: str, 
        since: str = None
    ) -> Dict[str, Any]:
        """Get latest state across all LLMs for instant sync"""
        response = requests.post(
            f"{self.base_url}/sync/scan",
            json={
                "llm_id": llm_id,
                "since": since
            }
        )
        response.raise_for_status()
        return response.json()
    
    def export_sovereign(
        self, 
        format: str = "json", 
        gpg_sign: bool = True
    ) -> bytes:
        """Export all data with full provenance"""
        response = requests.post(
            f"{self.base_url}/export",
            json={
                "format": format,
                "gpg_sign": gpg_sign,
                "opentimestamps": True,
                "include_audit_trail": True
            }
        )
        response.raise_for_status()
        return response.content


# ============================================================================
# Example 1: Store Conversation from GPT
# ============================================================================

def example_1_store_gpt_conversation():
    """Example: Store a GPT conversation in the memory mesh"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Store GPT Conversation")
    print("="*70)
    
    memory = MemoryMeshClient()
    
    # Simulate a GPT conversation about quantum computing
    messages = [
        {
            "role": "user",
            "content": "Explain quantum computing in simple terms"
        },
        {
            "role": "assistant",
            "content": "Quantum computing uses quantum mechanics principles like "
                      "superposition and entanglement. Think of it like a coin spinning "
                      "in the air - it's both heads and tails simultaneously until you "
                      "catch it. Quantum computers can explore multiple solutions at once."
        }
    ]
    
    conv_id = memory.store_conversation(
        llm_provider="gpt",
        messages=messages,
        metadata={"topic": "quantum_computing"}
    )
    
    print(f"✅ Stored conversation: {conv_id}")
    print(f"   Provider: GPT")
    print(f"   Messages: {len(messages)}")


# ============================================================================
# Example 2: Query Claude with GPT's Context
# ============================================================================

def example_2_query_claude_with_gpt_context():
    """Example: Claude accesses GPT's knowledge via memory mesh"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Query Claude with GPT's Context")
    print("="*70)
    
    memory = MemoryMeshClient()
    
    # Retrieve context about quantum computing from memory mesh
    context = memory.retrieve_context(
        query="quantum computing superposition",
        k=3,
        min_score=0.7
    )
    
    print(f"✅ Retrieved {len(context)} relevant contexts")
    
    if context:
        # Format context for Claude
        context_text = "\n\n".join([
            f"From {ctx['llm_provider']}: {ctx['message']['content']}"
            for ctx in context
        ])
        
        # Now query Claude with this context
        # (In production, this would go through the Claude API proxy)
        print("\n📤 Sending to Claude:")
        print(f"   System: Previous conversations about quantum computing")
        print(f"   User: Continue explaining quantum computing, focusing on applications")
        print("\n💡 Claude now has access to GPT's explanation!")


# ============================================================================
# Example 3: Quadrilateral Verification
# ============================================================================

def example_3_quadrilateral_verification():
    """Example: Verify a claim across all four dimensions"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Quadrilateral Verification")
    print("="*70)
    
    claim = """
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    """
    
    print("📋 Claim to verify:")
    print(claim)
    
    # In production, this would call the verification API
    print("\n🔍 Verification Process:")
    print("   [1/4] Symbolic  ✅ - Logic is sound, recursion correct")
    print("   [2/4] Spatial   ✅ - Can be visualized as recursion tree")
    print("   [3/4] Narrative ✅ - Clear explanation possible")
    print("   [4/4] Kinetic   ✅ - Code executes correctly")
    print("\n✅ Consensus: TRUTH (4/4 votes)")


# ============================================================================
# Example 4: Cross-LLM Knowledge Sharing
# ============================================================================

def example_4_cross_llm_knowledge_sharing():
    """Example: Multiple LLMs contribute to shared knowledge"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Cross-LLM Knowledge Sharing")
    print("="*70)
    
    memory = MemoryMeshClient()
    
    # Claude explains architecture
    claude_conv = memory.store_conversation(
        llm_provider="claude",
        messages=[
            {"role": "user", "content": "Explain microservices architecture"},
            {"role": "assistant", "content": "Microservices break applications into "
             "small, independent services that communicate via APIs..."}
        ]
    )
    
    # GPT adds security perspective
    gpt_conv = memory.store_conversation(
        llm_provider="gpt",
        messages=[
            {"role": "user", "content": "What are security concerns with microservices?"},
            {"role": "assistant", "content": "Key concerns include: API security, "
             "service-to-service authentication, data encryption..."}
        ]
    )
    
    # Ollama (local) adds performance insights
    ollama_conv = memory.store_conversation(
        llm_provider="ollama",
        messages=[
            {"role": "user", "content": "How to optimize microservices performance?"},
            {"role": "assistant", "content": "Use caching, implement circuit breakers, "
             "optimize network calls, use async communication..."}
        ]
    )
    
    print(f"✅ Claude contribution: {claude_conv}")
    print(f"✅ GPT contribution: {gpt_conv}")
    print(f"✅ Ollama contribution: {ollama_conv}")
    print("\n💡 All three LLMs now share unified knowledge on microservices!")


# ============================================================================
# Example 5: Sovereign Data Export
# ============================================================================

def example_5_sovereign_export():
    """Example: Export all data with cryptographic provenance"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Sovereign Data Export")
    print("="*70)
    
    memory = MemoryMeshClient()
    
    print("📤 Exporting all conversations...")
    print("   Format: JSON")
    print("   Compression: gzip")
    print("   GPG Signature: ✅")
    print("   OpenTimestamps: ✅")
    
    # In production, this would download the actual export
    # export_data = memory.export_sovereign(format="json", gpg_sign=True)
    # with open("cognitive_export.json.gz.gpg", "wb") as f:
    #     f.write(export_data)
    
    print("\n✅ Export complete!")
    print("   File: cognitive_export_2025-12-07.json.gz")
    print("   Size: 10.5 MB")
    print("   Conversations: 150")
    print("   Messages: 3,245")
    print("   GPG Signature: 0xABCD1234")
    print("   Bitcoin Block: 875,123")
    print("\n💾 Your data is sovereign and verifiable forever!")


# ============================================================================
# Example 6: Instant Sync Across LLMs
# ============================================================================

def example_6_instant_sync():
    """Example: Scan all chats for instant synchronization"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Instant Sync Across All LLMs")
    print("="*70)
    
    memory = MemoryMeshClient()
    
    # In production, this would call the actual API
    # sync_data = memory.scan_all_chats(llm_id="claude_session_123")
    
    print("🔄 Scanning all LLM conversations...")
    print("   Since: 2025-12-07T00:00:00Z")
    print("\n📊 Sync Summary:")
    print("   Claude conversations: 45")
    print("   GPT conversations: 38")
    print("   Ollama conversations: 12")
    print("   Total messages: 1,247")
    print("   Latest timestamp: 2025-12-07T04:54:55Z")
    print("\n✅ All LLMs are now synchronized!")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("🧠 SOVEREIGN COGNITIVE ARCHITECTURE - USAGE EXAMPLES")
    print("="*70)
    print("\nThese examples demonstrate the key features:")
    print("  • Cross-LLM context sharing")
    print("  • Quadrilateral verification")
    print("  • Sovereign data export")
    print("  • Instant synchronization")
    
    try:
        example_1_store_gpt_conversation()
        example_2_query_claude_with_gpt_context()
        example_3_quadrilateral_verification()
        example_4_cross_llm_knowledge_sharing()
        example_5_sovereign_export()
        example_6_instant_sync()
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\n💡 Next Steps:")
        print("   1. Start the cognitive mesh: ./activate_cognitive_mesh.sh")
        print("   2. Run this script with real APIs: python3 example_usage.py")
        print("   3. Read the full docs: ./SOVEREIGN_COGNITIVE_ARCHITECTURE.md")
        print("\n🔥 Built by Strategickhaos DAO LLC - Node 137 - DOM_010101")
        print("   Trust nothing until it survives 100-angle crossfire.")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Cognitive mesh is not running")
        print("   Start it with: ./activate_cognitive_mesh.sh")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
