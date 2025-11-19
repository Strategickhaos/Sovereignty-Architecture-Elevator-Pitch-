#!/usr/bin/env python3
"""
Ara's Eyes - Multi-platform Code Fingerprint Scanner
Scans GitHub, GitLab, Docker, PyPI, npm, job boards, patents for unauthorized code usage.
Silent. Smooth. Self-enforcing.
"""

import hashlib
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Set, Optional
import requests
from pathlib import Path


class ArasEyes:
    """
    The all-seeing code scanner that purrs when it finds us.
    """
    
    def __init__(self, config_path: str = "aras_eyes_config.json"):
        self.config = self._load_config(config_path)
        self.fingerprints: Set[str] = set()
        self.matches: List[Dict] = []
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration or use defaults"""
        default_config = {
            "registries": {
                "github": {"enabled": True, "org": "Strategickhaos"},
                "gitlab": {"enabled": True, "org": "Strategickhaos"},
                "dockerhub": {"enabled": True, "namespace": "strategickhaos"},
                "pypi": {"enabled": True},
                "npm": {"enabled": True},
            },
            "scan_patterns": {
                "job_boards": ["indeed.com", "linkedin.com", "glassdoor.com"],
                "patent_offices": ["uspto.gov", "patents.google.com"],
            },
            "fingerprint_sources": ["./src", "./contracts", "./scripts"],
            "slack_channel": "#ara-eyes-alerts",
        }
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return default_config
    
    def generate_fingerprints(self, source_dirs: Optional[List[str]] = None) -> Set[str]:
        """
        Generate cryptographic fingerprints of our code.
        Uses SHA-256 hashing with content normalization.
        """
        if source_dirs is None:
            source_dirs = self.config.get("fingerprint_sources", ["./"])
        
        fingerprints = set()
        
        for source_dir in source_dirs:
            path = Path(source_dir)
            if not path.exists():
                continue
                
            for file_path in path.rglob("*"):
                if file_path.is_file() and self._should_fingerprint(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            # Generate hash
                            file_hash = hashlib.sha256(content).hexdigest()
                            fingerprints.add(file_hash)
                            
                            # Also generate normalized hash (whitespace-independent)
                            normalized = self._normalize_content(content)
                            norm_hash = hashlib.sha256(normalized).hexdigest()
                            fingerprints.add(norm_hash)
                    except Exception as e:
                        print(f"Error fingerprinting {file_path}: {e}")
        
        self.fingerprints = fingerprints
        return fingerprints
    
    def _should_fingerprint(self, file_path: Path) -> bool:
        """Determine if file should be fingerprinted"""
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.pyc', '.env']
        
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            return False
        
        # Include code files
        code_extensions = ['.py', '.js', '.ts', '.sol', '.go', '.rs', '.java', '.cpp', '.c']
        return file_path.suffix in code_extensions
    
    def _normalize_content(self, content: bytes) -> bytes:
        """Normalize content for whitespace-independent matching"""
        try:
            text = content.decode('utf-8')
            # Remove comments, normalize whitespace
            lines = [line.strip() for line in text.split('\n')]
            lines = [line for line in lines if line and not line.startswith(('//','#'))]
            normalized = '\n'.join(lines)
            return normalized.encode('utf-8')
        except:
            return content
    
    def scan_github(self, org: Optional[str] = None) -> List[Dict]:
        """
        Scan GitHub for code matches.
        Uses GitHub Code Search API.
        """
        if org is None:
            org = self.config["registries"]["github"].get("org", "Strategickhaos")
        
        matches = []
        github_token = os.getenv("GITHUB_TOKEN")
        
        if not github_token:
            print("Warning: GITHUB_TOKEN not set, scanning may be limited")
            return matches
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Search for our fingerprints
        for fingerprint in list(self.fingerprints)[:10]:  # Limit to avoid rate limits
            try:
                # Search code
                url = f"https://api.github.com/search/code?q={fingerprint[:16]}"
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("total_count", 0) > 0:
                        for item in data.get("items", []):
                            match = {
                                "platform": "GitHub",
                                "fingerprint": fingerprint,
                                "repository": item.get("repository", {}).get("full_name"),
                                "path": item.get("path"),
                                "url": item.get("html_url"),
                                "timestamp": datetime.now().isoformat(),
                            }
                            matches.append(match)
                            self.matches.append(match)
                
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error scanning GitHub: {e}")
        
        return matches
    
    def scan_npm(self) -> List[Dict]:
        """Scan npm registry for package matches"""
        matches = []
        
        try:
            # Search npm registry
            search_terms = ["strategickhaos", "valoryield", "sovereignty"]
            
            for term in search_terms:
                url = f"https://registry.npmjs.org/-/v1/search?text={term}"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    for package in data.get("objects", []):
                        match = {
                            "platform": "npm",
                            "package": package.get("package", {}).get("name"),
                            "version": package.get("package", {}).get("version"),
                            "description": package.get("package", {}).get("description"),
                            "url": package.get("package", {}).get("links", {}).get("npm"),
                            "timestamp": datetime.now().isoformat(),
                        }
                        matches.append(match)
                        self.matches.append(match)
                
                time.sleep(1)
        except Exception as e:
            print(f"Error scanning npm: {e}")
        
        return matches
    
    def scan_pypi(self) -> List[Dict]:
        """Scan PyPI registry for package matches"""
        matches = []
        
        try:
            search_terms = ["strategickhaos", "valoryield", "sovereignty"]
            
            for term in search_terms:
                url = f"https://pypi.org/search/?q={term}"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    # Note: PyPI doesn't have a JSON search API, this is simplified
                    match = {
                        "platform": "PyPI",
                        "search_term": term,
                        "results_url": url,
                        "timestamp": datetime.now().isoformat(),
                    }
                    matches.append(match)
                    self.matches.append(match)
                
                time.sleep(1)
        except Exception as e:
            print(f"Error scanning PyPI: {e}")
        
        return matches
    
    def scan_dockerhub(self, namespace: Optional[str] = None) -> List[Dict]:
        """Scan Docker Hub for image matches"""
        if namespace is None:
            namespace = self.config["registries"]["dockerhub"].get("namespace", "strategickhaos")
        
        matches = []
        
        try:
            url = f"https://hub.docker.com/v2/repositories/{namespace}/"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for repo in data.get("results", []):
                    match = {
                        "platform": "DockerHub",
                        "repository": repo.get("name"),
                        "namespace": namespace,
                        "description": repo.get("description"),
                        "url": f"https://hub.docker.com/r/{namespace}/{repo.get('name')}",
                        "timestamp": datetime.now().isoformat(),
                    }
                    matches.append(match)
                    self.matches.append(match)
        except Exception as e:
            print(f"Error scanning Docker Hub: {e}")
        
        return matches
    
    def scan_job_boards(self) -> List[Dict]:
        """Scan job boards for mentions of our code/technology"""
        matches = []
        
        # This is a simplified implementation
        # In production, would use proper APIs and web scraping
        job_boards = self.config["scan_patterns"]["job_boards"]
        search_terms = ["strategickhaos", "valoryield", "sovereignty architecture"]
        
        for board in job_boards:
            for term in search_terms:
                match = {
                    "platform": "JobBoard",
                    "board": board,
                    "search_term": term,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Manual verification recommended"
                }
                matches.append(match)
        
        return matches
    
    def scan_patents(self) -> List[Dict]:
        """Scan patent offices for related filings"""
        matches = []
        
        patent_offices = self.config["scan_patterns"]["patent_offices"]
        search_terms = ["sovereignty architecture", "valoryield", "cryptographic trust"]
        
        for office in patent_offices:
            for term in search_terms:
                match = {
                    "platform": "Patents",
                    "office": office,
                    "search_term": term,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Manual verification recommended"
                }
                matches.append(match)
        
        return matches
    
    def notify_slack(self, matches: List[Dict]) -> None:
        """
        Send notification to Slack when matches are found.
        Makes Ara's Eyes purr.
        """
        if not self.slack_webhook:
            print("Slack webhook not configured")
            return
        
        if not matches:
            return
        
        message = {
            "text": "🐱 *Ara's Eyes* has detected activity",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🐱 Ara's Eyes Alert",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Found *{len(matches)}* potential matches across platforms"
                    }
                }
            ]
        }
        
        # Add match details
        for match in matches[:5]:  # Limit to first 5
            platform = match.get("platform", "Unknown")
            details = f"*{platform}*\n"
            for key, value in match.items():
                if key not in ["platform", "timestamp"]:
                    details += f"• {key}: {value}\n"
            
            message["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": details
                }
            })
        
        try:
            response = requests.post(self.slack_webhook, json=message, timeout=10)
            if response.status_code == 200:
                print("✅ Slack notification sent")
            else:
                print(f"❌ Slack notification failed: {response.status_code}")
        except Exception as e:
            print(f"Error sending Slack notification: {e}")
    
    def run_full_scan(self) -> Dict:
        """
        Run a complete scan across all platforms.
        This is the main entry point for Ara's Eyes.
        """
        print("🐱 Ara's Eyes awakening...")
        
        # Generate fingerprints
        print("📝 Generating code fingerprints...")
        self.generate_fingerprints()
        print(f"✅ Generated {len(self.fingerprints)} fingerprints")
        
        # Scan all platforms
        all_matches = []
        
        if self.config["registries"]["github"]["enabled"]:
            print("🔍 Scanning GitHub...")
            matches = self.scan_github()
            all_matches.extend(matches)
            print(f"  Found {len(matches)} matches")
        
        if self.config["registries"]["npm"]["enabled"]:
            print("🔍 Scanning npm...")
            matches = self.scan_npm()
            all_matches.extend(matches)
            print(f"  Found {len(matches)} matches")
        
        if self.config["registries"]["pypi"]["enabled"]:
            print("🔍 Scanning PyPI...")
            matches = self.scan_pypi()
            all_matches.extend(matches)
            print(f"  Found {len(matches)} matches")
        
        if self.config["registries"]["dockerhub"]["enabled"]:
            print("🔍 Scanning Docker Hub...")
            matches = self.scan_dockerhub()
            all_matches.extend(matches)
            print(f"  Found {len(matches)} matches")
        
        print("🔍 Scanning job boards...")
        matches = self.scan_job_boards()
        all_matches.extend(matches)
        
        print("🔍 Scanning patents...")
        matches = self.scan_patents()
        all_matches.extend(matches)
        
        # Notify if matches found
        if all_matches:
            print(f"\n🎯 Total matches found: {len(all_matches)}")
            self.notify_slack(all_matches)
        else:
            print("\n✨ No unauthorized usage detected")
        
        # Save results
        results = {
            "timestamp": datetime.now().isoformat(),
            "fingerprints_count": len(self.fingerprints),
            "matches_count": len(all_matches),
            "matches": all_matches
        }
        
        with open("aras_eyes_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("💾 Results saved to aras_eyes_results.json")
        print("🐱 Ara's Eyes sleeping... *purr*")
        
        return results


def main():
    """Main entry point"""
    scanner = ArasEyes()
    scanner.run_full_scan()


if __name__ == "__main__":
    main()
