"""
API Recon Capture Module
Captures API traffic from browser DevTools and proxy traffic
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse
import json
import re
import hashlib
from dataclasses import dataclass, asdict


@dataclass
class APIPattern:
    """Represents a captured API pattern"""
    method: str
    url: str
    path: str
    params: Dict[str, Any]
    headers: Dict[str, str]
    body: Optional[str]
    response_status: Optional[int]
    response_headers: Optional[Dict[str, str]]
    response_body_sample: Optional[str]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def get_id(self) -> str:
        """Generate unique ID for this pattern"""
        content = f"{self.method}:{self.path}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class APIReconCapture:
    """
    Captures and normalizes API traffic patterns
    Can work with mitmproxy, HAR files, or manual captures
    """
    
    def __init__(self, qdrant_client=None, encoder=None):
        self.qdrant = qdrant_client
        self.encoder = encoder
        self.captured: List[APIPattern] = []
        self.cloud_domains = [
            "googleapis.com",
            "clients6.google.com", 
            "cloud.google.com",
            "azure.com",
            "amazonaws.com",
            "cloudconsole-pa.clients6.google.com",
            "monitoring.clients6.google.com",
            "shell.cloud.google.com"
        ]
    
    def is_cloud_api(self, url: str) -> bool:
        """Check if URL is a cloud provider API"""
        return any(domain in url for domain in self.cloud_domains)
    
    def extract_path(self, url: str) -> str:
        """Extract and normalize API path pattern"""
        parsed = urlparse(url)
        path = parsed.path
        
        # Replace project IDs with {project}
        path = re.sub(r'/projects/[^/]+/', '/projects/{project}/', path)
        
        # Replace numeric IDs with {id}
        path = re.sub(r'/\d+/', '/{id}/', path)
        
        # Replace UUIDs with {uuid}
        uuid_pattern = r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/'
        path = re.sub(uuid_pattern, '/{uuid}/', path, flags=re.IGNORECASE)
        
        return path
    
    def parse_har_file(self, har_path: str) -> List[APIPattern]:
        """Parse HAR file from browser DevTools"""
        with open(har_path, 'r') as f:
            har_data = json.load(f)
        
        patterns = []
        for entry in har_data.get('log', {}).get('entries', []):
            request = entry.get('request', {})
            response = entry.get('response', {})
            url = request.get('url', '')
            
            if not self.is_cloud_api(url):
                continue
            
            # Extract headers
            headers = {h['name']: h['value'] for h in request.get('headers', [])}
            response_headers = {h['name']: h['value'] for h in response.get('headers', [])}
            
            # Extract params
            params = {p['name']: p['value'] for p in request.get('queryString', [])}
            
            # Extract body
            body = None
            if 'postData' in request:
                body = request['postData'].get('text', '')
            
            # Extract response body sample
            response_body = None
            if 'content' in response:
                content = response['content'].get('text', '')
                response_body = content[:1000] if content else None
            
            pattern = APIPattern(
                method=request.get('method', 'GET'),
                url=url,
                path=self.extract_path(url),
                params=params,
                headers=headers,
                body=body,
                response_status=response.get('status'),
                response_headers=response_headers,
                response_body_sample=response_body,
                timestamp=entry.get('startedDateTime', datetime.now(timezone.utc).isoformat())
            )
            
            patterns.append(pattern)
            self.captured.append(pattern)
        
        return patterns
    
    def vectorize_and_store(self, pattern: APIPattern) -> bool:
        """Vectorize pattern and store in Qdrant"""
        if not self.qdrant or not self.encoder:
            return False
        
        try:
            # Create embedding from pattern
            pattern_text = json.dumps({
                "method": pattern.method,
                "path": pattern.path,
                "params": pattern.params,
                "description": self._infer_description(pattern)
            })
            
            embedding = self.encoder.encode(pattern_text)
            
            # Store in Qdrant
            self.qdrant.upsert(
                collection_name="api_patterns",
                points=[{
                    "id": pattern.get_id(),
                    "vector": embedding.tolist(),
                    "payload": pattern.to_dict()
                }]
            )
            
            return True
        except Exception as e:
            print(f"Error vectorizing pattern: {e}")
            return False
    
    def _infer_description(self, pattern: APIPattern) -> str:
        """Infer human-readable description from pattern"""
        path = pattern.path
        method = pattern.method
        
        # Simple heuristics
        if 'metric' in path.lower():
            return f"{method} metrics data"
        elif 'group' in path.lower():
            return f"{method} resource groups"
        elif 'descriptor' in path.lower():
            return f"{method} resource descriptors"
        elif 'quota' in path.lower():
            return f"{method} quota information"
        elif 'operations' in path.lower():
            return f"{method} operations status"
        else:
            return f"{method} {path.split('/')[-1] or 'resource'}"
    
    def save_to_file(self, output_path: str) -> None:
        """Save captured patterns to JSON file"""
        data = {
            "capture_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_patterns": len(self.captured),
            "patterns": [p.to_dict() for p in self.captured]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(self.captured)} patterns to {output_path}")
    
    def load_from_file(self, input_path: str) -> List[APIPattern]:
        """Load patterns from JSON file"""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        patterns = []
        for p in data.get('patterns', []):
            pattern = APIPattern(**p)
            patterns.append(pattern)
            self.captured.append(pattern)
        
        print(f"Loaded {len(patterns)} patterns from {input_path}")
        return patterns


def main():
    """CLI interface for API capture"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Capture API patterns from HAR files')
    parser.add_argument('har_file', help='Path to HAR file from browser DevTools')
    parser.add_argument('-o', '--output', default='captured_patterns.json',
                       help='Output JSON file')
    parser.add_argument('--vectorize', action='store_true',
                       help='Vectorize and store in Qdrant')
    parser.add_argument('--qdrant-host', default=os.getenv('QDRANT_HOST', 'localhost'),
                       help='Qdrant host (default: localhost or QDRANT_HOST env var)')
    parser.add_argument('--qdrant-port', type=int, default=int(os.getenv('QDRANT_PORT', '6333')),
                       help='Qdrant port (default: 6333 or QDRANT_PORT env var)')
    
    args = parser.parse_args()
    
    # Initialize capture
    qdrant_client = None
    encoder = None
    
    if args.vectorize:
        try:
            from qdrant_client import QdrantClient
            from sentence_transformers import SentenceTransformer
            
            qdrant_client = QdrantClient(args.qdrant_host, port=args.qdrant_port)
            encoder = SentenceTransformer('all-MiniLM-L6-v2')
            print(f"Qdrant initialized at {args.qdrant_host}:{args.qdrant_port}")
        except Exception as e:
            print(f"Warning: Could not initialize Qdrant: {e}")
    
    capture = APIReconCapture(qdrant_client, encoder)
    
    # Parse HAR file
    print(f"Parsing HAR file: {args.har_file}")
    patterns = capture.parse_har_file(args.har_file)
    
    print(f"Captured {len(patterns)} API patterns")
    
    # Vectorize if requested
    if args.vectorize and qdrant_client:
        print("Vectorizing patterns...")
        for pattern in patterns:
            capture.vectorize_and_store(pattern)
        print("Vectorization complete")
    
    # Save to file
    capture.save_to_file(args.output)
    
    # Print summary
    print("\n=== Capture Summary ===")
    print(f"Total patterns: {len(patterns)}")
    unique_paths = set(p.path for p in patterns)
    print(f"Unique paths: {len(unique_paths)}")
    for path in sorted(unique_paths):
        methods = set(p.method for p in patterns if p.path == path)
        print(f"  {', '.join(methods)} {path}")


if __name__ == "__main__":
    main()
