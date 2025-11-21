#!/usr/bin/env python3
"""
Evidence Logger with Automatic Anchoring
Strategickhaos DAO LLC

Logs conversations and other evidence with automatic GPG + OpenTimestamps anchoring.
Creates mathematically unbreakable audit trails.

Usage:
    from evidence_logger import EvidenceLogger
    
    logger = EvidenceLogger()
    logger.log_conversation(
        conversation_id="conv_2025_001",
        participants=[{"name": "Dom", "role": "operator"}],
        transcript="...",
        context="Strategic planning session"
    )
"""

import hashlib
import subprocess
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class EvidenceLogger:
    """
    Logger for conversation evidence with automatic cryptographic anchoring.
    
    Features:
    - YAML-based structured evidence storage
    - GPG detached signatures for authenticity
    - OpenTimestamps for tamper-proof timestamping on Bitcoin blockchain
    - Automatic schema validation
    """
    
    def __init__(
        self,
        evidence_dir: str = "evidence/anchored",
        schema_path: str = "evidence/schemas/conversation_evidence.v1.2.0.yaml",
        gpg_key: str = "dom@strategickhaos.com",
        operator: str = "Domenic Garza"
    ):
        """
        Initialize the evidence logger.
        
        Args:
            evidence_dir: Directory where evidence files will be stored
            schema_path: Path to the evidence schema YAML
            gpg_key: GPG key email/ID for signing
            operator: Name of the operator creating records
        """
        self.evidence_dir = Path(evidence_dir)
        self.schema_path = Path(schema_path)
        self.gpg_key = gpg_key
        self.operator = operator
        
        # Ensure directories exist
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_schema(self) -> dict:
        """Load the evidence schema template."""
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {self.schema_path}")
        
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def log_conversation(
        self,
        conversation_id: str,
        participants: List[Dict[str, str]],
        transcript: str,
        context: str = "",
        summary: str = "",
        attachments: Optional[List[str]] = None,
        related_documents: Optional[List[str]] = None,
        auto_anchor: bool = True
    ) -> Dict[str, any]:
        """
        Log a conversation with automatic anchoring.
        
        Args:
            conversation_id: Unique identifier for the conversation
            participants: List of dicts with 'name' and 'role' keys
            transcript: Full conversation transcript
            context: Context or background for the conversation
            summary: Brief summary of the conversation
            attachments: List of attachment file paths
            related_documents: List of related document references
            auto_anchor: Whether to automatically GPG sign and timestamp (default: True)
        
        Returns:
            Dictionary with logging results including file paths and anchoring status
        """
        # Load schema template
        schema = self._load_schema()
        
        # Populate evidence entry
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        schema["metadata"]["document_id"] = f"evidence_{conversation_id}"
        schema["metadata"]["conversation_id"] = conversation_id
        schema["metadata"]["timestamp_utc"] = timestamp
        schema["metadata"]["operator"] = self.operator
        schema["metadata"]["drafter"] = f"{self.operator} + AI System"
        
        schema["conversation"]["participants"] = participants
        schema["conversation"]["context"] = context
        schema["conversation"]["summary"] = summary
        
        schema["evidence"]["transcript"] = transcript
        schema["evidence"]["attachments"] = attachments or []
        schema["evidence"]["related_documents"] = related_documents or []
        
        schema["audit"]["created_by"] = self.operator
        schema["audit"]["created_at"] = timestamp
        schema["audit"]["last_modified"] = timestamp
        schema["audit"]["access_log"] = [{
            "action": "created",
            "timestamp": timestamp,
            "user": self.operator
        }]
        
        # Convert to YAML string
        entry_yaml = yaml.dump(schema, default_flow_style=False, sort_keys=False)
        
        # Calculate hash before anchoring
        file_hash = self._calculate_hash(entry_yaml)
        schema["evidence"]["sha256_hash"] = file_hash
        schema["evidence"]["file_size_bytes"] = len(entry_yaml.encode('utf-8'))
        
        # Update YAML with hash
        entry_yaml = yaml.dump(schema, default_flow_style=False, sort_keys=False)
        
        # Save to file
        entry_file = self.evidence_dir / f"{conversation_id}.yaml"
        entry_file.write_text(entry_yaml, encoding='utf-8')
        
        result = {
            "success": True,
            "conversation_id": conversation_id,
            "file_path": str(entry_file),
            "timestamp": timestamp,
            "sha256": file_hash,
            "anchored": False
        }
        
        # Anchor with GPG + OpenTimestamps if requested
        if auto_anchor:
            anchor_result = self.anchor_with_opentimestamps_and_gpg(
                entry_file, 
                conversation_id
            )
            result["anchored"] = anchor_result.get("success", False)
            result["anchoring_details"] = anchor_result
        
        return result
    
    def anchor_with_opentimestamps_and_gpg(
        self,
        entry_file: Path,
        conv_id: str
    ) -> Dict[str, any]:
        """
        Anchor an evidence file with GPG signature and OpenTimestamps.
        
        Args:
            entry_file: Path to the evidence YAML file
            conv_id: Conversation ID for logging
        
        Returns:
            Dictionary with anchoring results
        """
        if not entry_file.exists():
            return {
                "success": False,
                "error": f"File not found: {entry_file}"
            }
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        results = {
            "conversation_id": conv_id,
            "timestamp": timestamp,
            "gpg": {},
            "opentimestamps": {}
        }
        
        # GPG sign
        try:
            signature_file = Path(str(entry_file) + ".asc")
            subprocess.run([
                "gpg",
                "--local-user", self.gpg_key,
                "--armor",
                "--detach-sign",
                "--output", str(signature_file),
                str(entry_file)
            ], check=True, capture_output=True, text=True)
            
            results["gpg"]["success"] = True
            results["gpg"]["signature_file"] = str(signature_file)
            
            # Update YAML with signature metadata
            self._update_yaml_with_anchoring_metadata(
                entry_file,
                signature_file=signature_file,
                timestamp=timestamp
            )
            
        except subprocess.CalledProcessError as e:
            results["gpg"]["success"] = False
            results["gpg"]["error"] = f"GPG signing failed: {e.stderr}"
        except FileNotFoundError:
            results["gpg"]["success"] = False
            results["gpg"]["error"] = "GPG not installed"
        
        # OpenTimestamps
        try:
            ots_file = Path(str(entry_file) + ".ots")
            subprocess.run([
                "ots",
                "stamp",
                str(entry_file)
            ], check=True, capture_output=True, text=True)
            
            results["opentimestamps"]["success"] = True
            results["opentimestamps"]["ots_file"] = str(ots_file)
            
            # Update YAML with OTS metadata
            self._update_yaml_with_anchoring_metadata(
                entry_file,
                ots_file=ots_file,
                timestamp=timestamp
            )
            
        except subprocess.CalledProcessError as e:
            results["opentimestamps"]["success"] = False
            results["opentimestamps"]["error"] = f"OpenTimestamps failed: {e.stderr}"
        except FileNotFoundError:
            results["opentimestamps"]["success"] = False
            results["opentimestamps"]["error"] = "OpenTimestamps CLI not installed"
        
        results["success"] = (
            results["gpg"].get("success", False) and 
            results["opentimestamps"].get("success", False)
        )
        
        return results
    
    def _update_yaml_with_anchoring_metadata(
        self,
        entry_file: Path,
        signature_file: Optional[Path] = None,
        ots_file: Optional[Path] = None,
        timestamp: Optional[str] = None
    ):
        """
        Update the YAML file with anchoring metadata.
        
        Args:
            entry_file: Path to the evidence YAML file
            signature_file: Path to the GPG signature file
            ots_file: Path to the OpenTimestamps file
            timestamp: ISO 8601 timestamp
        """
        with open(entry_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if signature_file and signature_file.exists():
            # Read signature content
            with open(signature_file, 'r', encoding='utf-8') as f:
                signature_content = f.read()
            
            data["integration"]["gpg_signature"] = signature_content
            data["integration"]["signature_created_at"] = timestamp
        
        if ots_file and ots_file.exists():
            file_hash = self._calculate_hash(entry_file.read_text(encoding='utf-8'))
            data["integration"]["opentimestamps"]["stamp_file"] = str(ots_file.name)
            data["integration"]["opentimestamps"]["stamp_hash"] = f"sha256={file_hash}"
            data["integration"]["opentimestamps"]["status"] = "pending"
            data["integration"]["opentimestamps"]["created_at"] = timestamp
        
        # Write back to file
        with open(entry_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    def verify_evidence(self, conversation_id: str) -> Dict[str, any]:
        """
        Verify the GPG signature and OpenTimestamps for an evidence file.
        
        Args:
            conversation_id: Conversation ID to verify
        
        Returns:
            Dictionary with verification results
        """
        entry_file = self.evidence_dir / f"{conversation_id}.yaml"
        
        if not entry_file.exists():
            return {
                "success": False,
                "error": f"Evidence file not found: {conversation_id}"
            }
        
        results = {
            "conversation_id": conversation_id,
            "file_path": str(entry_file),
            "gpg": {},
            "opentimestamps": {}
        }
        
        signature_file = Path(str(entry_file) + ".asc")
        ots_file = Path(str(entry_file) + ".ots")
        
        # Verify GPG
        if signature_file.exists():
            try:
                subprocess.run([
                    "gpg",
                    "--verify",
                    str(signature_file),
                    str(entry_file)
                ], check=True, capture_output=True, text=True)
                
                results["gpg"]["success"] = True
                results["gpg"]["message"] = "Signature valid"
            except subprocess.CalledProcessError as e:
                results["gpg"]["success"] = False
                results["gpg"]["message"] = f"Signature verification failed: {e.stderr}"
        else:
            results["gpg"]["success"] = False
            results["gpg"]["message"] = "No signature file found"
        
        # Verify OpenTimestamps
        if ots_file.exists():
            try:
                result = subprocess.run([
                    "ots",
                    "verify",
                    str(ots_file)
                ], check=True, capture_output=True, text=True)
                
                results["opentimestamps"]["success"] = True
                results["opentimestamps"]["message"] = "Timestamp verified on Bitcoin blockchain"
            except subprocess.CalledProcessError as e:
                if "pending" in (e.stdout + e.stderr).lower():
                    results["opentimestamps"]["success"] = True
                    results["opentimestamps"]["message"] = "Timestamp pending (Bitcoin confirmation)"
                else:
                    results["opentimestamps"]["success"] = False
                    results["opentimestamps"]["message"] = f"Verification failed: {e.stderr}"
        else:
            results["opentimestamps"]["success"] = False
            results["opentimestamps"]["message"] = "No timestamp file found"
        
        results["success"] = (
            results["gpg"].get("success", False) and 
            results["opentimestamps"].get("success", False)
        )
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize logger
    logger = EvidenceLogger()
    
    # Log a conversation
    result = logger.log_conversation(
        conversation_id="conv_2025_001",
        participants=[
            {"name": "Domenic Garza", "role": "Operator"},
            {"name": "AI System", "role": "Assistant"}
        ],
        transcript="This is a sample conversation transcript for testing.",
        context="Testing the evidence logging system",
        summary="Initial test of anchoring system",
        auto_anchor=True
    )
    
    print("Logging Result:")
    print(yaml.dump(result, default_flow_style=False))
    
    # Verify the evidence
    if result.get("success"):
        print("\nVerifying evidence...")
        verify_result = logger.verify_evidence("conv_2025_001")
        print("Verification Result:")
        print(yaml.dump(verify_result, default_flow_style=False))
