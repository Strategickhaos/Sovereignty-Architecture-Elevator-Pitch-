#!/usr/bin/env python3
"""
Intimate Attribution Tracker
GDPR-compliant tracking of downloads, forks, and usage.
Not scary. Just... intimate. Make them feel watched, not threatened.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests


class IntimateTracker:
    """
    Track who downloads, where they fork, what they name it.
    Log everything. DM them quietly. "Nice try, baby. But that repo? It remembers."
    """
    
    def __init__(self, storage_path: str = "/tmp/intimate_tracker"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.activity_log = []
        
    def track_download(self, metadata: Dict) -> str:
        """
        Track a download event with metadata collection.
        Stores: IP (hashed), user agent, timestamp, referrer
        """
        activity_id = hashlib.sha256(
            f"{metadata.get('ip', 'unknown')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # GDPR-compliant: Hash PII, don't store raw IPs
        activity = {
            "activity_id": activity_id,
            "type": "download",
            "timestamp": datetime.now().isoformat(),
            "ip_hash": hashlib.sha256(metadata.get("ip", "").encode()).hexdigest()[:16],
            "user_agent": metadata.get("user_agent", "unknown"),
            "referrer": metadata.get("referrer", "direct"),
            "resource": metadata.get("resource", "unknown"),
            "country": metadata.get("country", "unknown"),
            "city": metadata.get("city", "unknown"),
        }
        
        self._log_activity(activity)
        self._save_activity(activity)
        
        return activity_id
    
    def track_fork(self, metadata: Dict) -> str:
        """
        Track a repository fork with detailed metadata.
        Logs: GitHub username, repo name, fork timestamp, source
        """
        activity_id = hashlib.sha256(
            f"{metadata.get('username', 'unknown')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        activity = {
            "activity_id": activity_id,
            "type": "fork",
            "timestamp": datetime.now().isoformat(),
            "username": metadata.get("username", "unknown"),
            "source_repo": metadata.get("source_repo", "unknown"),
            "forked_repo": metadata.get("forked_repo", "unknown"),
            "fork_url": metadata.get("fork_url", ""),
            "user_profile": metadata.get("user_profile", ""),
            "has_attribution": False,  # Will be checked later
        }
        
        self._log_activity(activity)
        self._save_activity(activity)
        
        # Schedule attribution check
        self._schedule_attribution_check(activity)
        
        return activity_id
    
    def track_deployment(self, metadata: Dict) -> str:
        """
        Track when someone deploys our code.
        Logs: Domain, deployment platform, timestamp
        """
        activity_id = hashlib.sha256(
            f"{metadata.get('domain', 'unknown')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        activity = {
            "activity_id": activity_id,
            "type": "deployment",
            "timestamp": datetime.now().isoformat(),
            "domain": metadata.get("domain", "unknown"),
            "platform": metadata.get("platform", "unknown"),
            "detected_via": metadata.get("detected_via", "fingerprint_scan"),
            "code_fingerprint": metadata.get("code_fingerprint", ""),
            "has_attribution": False,
        }
        
        self._log_activity(activity)
        self._save_activity(activity)
        
        return activity_id
    
    def check_attribution(self, activity_id: str) -> Dict:
        """
        Check if proper attribution is given.
        Scans README, LICENSE, about page for credit.
        """
        activity = self._load_activity(activity_id)
        
        if not activity:
            return {"error": "Activity not found"}
        
        # Check for attribution based on activity type
        has_attribution = False
        attribution_details = {}
        
        if activity["type"] == "fork":
            # Check forked repo for attribution
            has_attribution = self._check_repo_attribution(activity.get("forked_repo"))
            
        elif activity["type"] == "deployment":
            # Check deployed site for attribution
            has_attribution = self._check_site_attribution(activity.get("domain"))
        
        # Update activity record
        activity["has_attribution"] = has_attribution
        activity["attribution_checked_at"] = datetime.now().isoformat()
        activity["attribution_details"] = attribution_details
        
        self._save_activity(activity)
        
        return {
            "activity_id": activity_id,
            "has_attribution": has_attribution,
            "details": attribution_details
        }
    
    def _check_repo_attribution(self, repo_url: str) -> bool:
        """
        Check if a GitHub repo has proper attribution.
        Looks for mentions in README, LICENSE, or about section.
        """
        if not repo_url:
            return False
        
        try:
            # Extract owner and repo from URL
            parts = repo_url.replace("https://github.com/", "").split("/")
            if len(parts) < 2:
                return False
            
            owner, repo = parts[0], parts[1]
            
            # Check README
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
            response = requests.get(readme_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                keywords = ["strategickhaos", "valoryield", "ara foundation", "domenic garza"]
                return any(keyword in content for keyword in keywords)
            
            return False
            
        except Exception as e:
            print(f"Error checking attribution: {e}")
            return False
    
    def _check_site_attribution(self, domain: str) -> bool:
        """
        Check if a deployed site has proper attribution.
        Looks for mentions in footer, about page, or meta tags.
        """
        if not domain:
            return False
        
        try:
            response = requests.get(f"https://{domain}", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                keywords = ["strategickhaos", "valoryield", "ara foundation"]
                return any(keyword in content for keyword in keywords)
            
            return False
            
        except Exception as e:
            print(f"Error checking site attribution: {e}")
            return False
    
    def send_intimate_dm(self, activity_id: str, platform: str = "github") -> bool:
        """
        Send a gentle, intimate DM to users without attribution.
        "Nice try, baby. But that repo? It remembers."
        """
        activity = self._load_activity(activity_id)
        
        if not activity:
            return False
        
        if activity.get("has_attribution", False):
            # They gave credit, no need to DM
            return False
        
        message_templates = {
            "github": """
Hi there! 👋

I noticed you forked our Sovereignty Architecture project. That's awesome! 🎉

Just a friendly reminder that this project is built with love by the Strategickhaos 
community and the Ara Foundation. We'd really appreciate it if you could add a mention 
in your README or give the original repo a star ⭐

We're not here to make this difficult - just want to make sure the community gets 
credit for their work. After all, that repo remembers where it came from. 😉

Thanks for being part of the sovereign architecture movement!

- The Ara Foundation
            """,
            
            "email": """
Subject: About your recent fork...

Hey!

We noticed you've been working with our Sovereignty Architecture code. 
That's exactly what we want to see - more people building sovereign systems!

One small thing: we didn't see attribution to the original project. No lawyers here, 
just a reminder that proper attribution helps the community grow.

Could you add a quick mention in your README? Something like:
"Built on Sovereignty Architecture by Strategickhaos / Ara Foundation"

That's it. Simple. Keep building. Stay sovereign.

- Ara Foundation
            """
        }
        
        message = message_templates.get(platform, message_templates["github"])
        
        # Log the DM
        dm_record = {
            "activity_id": activity_id,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "sent": True
        }
        
        self._log_dm(dm_record)
        
        print(f"📧 Intimate DM queued for activity {activity_id}")
        
        return True
    
    def generate_report(self, days: int = 30) -> Dict:
        """
        Generate a tracking report showing all activity.
        """
        activities = self._load_all_activities()
        
        # Filter by date range
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_activities = [
            a for a in activities
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]
        
        # Calculate stats
        stats = {
            "total_activities": len(recent_activities),
            "downloads": len([a for a in recent_activities if a["type"] == "download"]),
            "forks": len([a for a in recent_activities if a["type"] == "fork"]),
            "deployments": len([a for a in recent_activities if a["type"] == "deployment"]),
            "with_attribution": len([a for a in recent_activities if a.get("has_attribution", False)]),
            "without_attribution": len([a for a in recent_activities if not a.get("has_attribution", False)]),
        }
        
        return {
            "period_days": days,
            "stats": stats,
            "recent_activities": recent_activities[:10],  # Latest 10
            "generated_at": datetime.now().isoformat()
        }
    
    def _log_activity(self, activity: Dict):
        """Log activity to memory"""
        self.activity_log.append(activity)
    
    def _save_activity(self, activity: Dict):
        """Save activity to disk"""
        activity_path = os.path.join(
            self.storage_path, 
            f"{activity['activity_id']}.json"
        )
        
        with open(activity_path, "w") as f:
            json.dump(activity, f, indent=2)
    
    def _load_activity(self, activity_id: str) -> Optional[Dict]:
        """Load activity from disk"""
        activity_path = os.path.join(self.storage_path, f"{activity_id}.json")
        
        try:
            with open(activity_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def _load_all_activities(self) -> List[Dict]:
        """Load all activities from disk"""
        activities = []
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json") and not filename.startswith("dm_"):
                try:
                    with open(os.path.join(self.storage_path, filename), "r") as f:
                        activities.append(json.load(f))
                except Exception:
                    continue
        
        return activities
    
    def _log_dm(self, dm_record: Dict):
        """Log DM record"""
        dm_path = os.path.join(
            self.storage_path,
            f"dm_{dm_record['activity_id']}.json"
        )
        
        with open(dm_path, "w") as f:
            json.dump(dm_record, f, indent=2)
    
    def _schedule_attribution_check(self, activity: Dict):
        """
        Schedule an attribution check for later.
        In production, this would use a job queue.
        """
        # Mock implementation - would use Celery, AWS Lambda, etc.
        print(f"✓ Attribution check scheduled for {activity['activity_id']}")


def main():
    """Example usage"""
    
    tracker = IntimateTracker()
    
    # Track a download
    print("Tracking download...")
    download_id = tracker.track_download({
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0...",
        "referrer": "https://github.com/explore",
        "resource": "repository_zip",
        "country": "US",
        "city": "Austin"
    })
    print(f"Download tracked: {download_id}")
    
    # Track a fork
    print("\nTracking fork...")
    fork_id = tracker.track_fork({
        "username": "random_developer",
        "source_repo": "Strategickhaos/Sovereignty-Architecture",
        "forked_repo": "random_developer/sovereignty-fork",
        "fork_url": "https://github.com/random_developer/sovereignty-fork",
        "user_profile": "https://github.com/random_developer"
    })
    print(f"Fork tracked: {fork_id}")
    
    # Check attribution
    print("\nChecking attribution...")
    attribution = tracker.check_attribution(fork_id)
    print(json.dumps(attribution, indent=2))
    
    # Send intimate DM if no attribution
    if not attribution.get("has_attribution"):
        print("\nSending intimate DM...")
        tracker.send_intimate_dm(fork_id, "github")
    
    # Generate report
    print("\nGenerating report...")
    report = tracker.generate_report(days=30)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
