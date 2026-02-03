import os
import subprocess
import json
import datetime

# Config
MANIFEST_FILE = "boot_manifest.json"  # In repo root
REPORT_FILE = "BOOT_REPORT.md"
MAX_CHARS_PER_FILE = 12000  # Truncate long docs

def find_repo_root(start_dir=os.getcwd()):
    """Walk up until .git found"""
    current = start_dir
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    raise FileNotFoundError("No .git found - not in repo?")

def run_git_cmd(cmd, repo_root):
    """Run git cmd in repo"""
    try:
        return subprocess.check_output(cmd, cwd=repo_root, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return "ERROR: Git cmd failed"

def get_git_stats(repo_root):
    """Commit count, last commit, open PRs (local approx), recent changes"""
    commits = run_git_cmd("git rev-list --all --count", repo_root)
    last_commit = run_git_cmd("git log -1 --format='%ci'", repo_root)
    open_prs_approx = run_git_cmd("git branch -r | grep pr/ | wc -l", repo_root)  # Approx; use API for real
    files_changed_7d = run_git_cmd("git log --name-only --since='7 days ago' | grep -v '^commit' | sort | uniq | wc -l", repo_root)
    return {
        "commits": int(commits) if commits.isdigit() else 0,
        "last_commit": last_commit,
        "open_prs_approx": int(open_prs_approx) if open_prs_approx.isdigit() else 0,
        "files_changed_7d": int(files_changed_7d) if files_changed_7d.isdigit() else 0,
    }

def load_manifest(manifest_path):
    """Load boot_manifest.json"""
    if not os.path.exists(manifest_path):
        return {"anchors": ["README.md"], "globs": []}  # Fallback
    with open(manifest_path, 'r') as f:
        return json.load(f)

def read_anchor(file_path):
    """Read file, truncate if long"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content[:MAX_CHARS_PER_FILE] + ('...' if len(content) > MAX_CHARS_PER_FILE else '')
    return "FILE NOT FOUND"

def generate_digest(repo_root, manifest, fast_mode=False):
    """Core digest gen"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats = get_git_stats(repo_root) if not fast_mode else get_git_stats(repo_root)  # Git always, even fast

    digest = f"# SAGCO BOOT DIGEST\nGenerated: {now}\nRepo: {os.path.basename(repo_root)}\n\n"

    # Stats section
    digest += "## System Stats\n"
    digest += f"- Total Commits: {stats['commits']}\n"
    digest += f"- Last Commit: {stats['last_commit']}\n"
    digest += f"- Open PRs (approx): {stats['open_prs_approx']}\n"
    digest += f"- Files Changed (7d): {stats['files_changed_7d']}\n\n"

    if fast_mode:
        digest += "## Fast Mode: Stats Only (No Doc Load)\nSTATUS: CONFIDENCE_OK\n"
        return digest

    # Anchors section
    anchors = manifest.get("anchors", [])
    digest += "## Anchor Docs\n"
    for anchor in anchors:
        full_path = os.path.join(repo_root, anchor)
        content = read_anchor(full_path)
        digest += f"### {anchor}\n{content}\n\n"

    # Globs (optional, skipped in fast)
    globs = manifest.get("globs", [])
    if globs:
        digest += "## Glob Matches\n"
        for glob in globs:
            # Simple glob sim (expand if needed)
            matches = [f for f in os.listdir(repo_root) if f.endswith('.md')]  # Demo; use glob module
            for match in matches[:manifest.get("max_files", 5)]:
                full_path = os.path.join(repo_root, match)
                content = read_anchor(full_path)
                digest += f"### {match}\n{content}\n\n"

    digest += "## STATUS: CONFIDENCE_OK\nNext: Merge open PRs + validate"

    return digest

def main(fast_mode=False):
    repo_root = find_repo_root()
    manifest_path = os.path.join(repo_root, MANIFEST_FILE)
    manifest = load_manifest(manifest_path)
    digest = generate_digest(repo_root, manifest, fast_mode)

    # Write report
    report_path = os.path.join(repo_root, REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(digest)

    # Console summary (short)
    print("SAGCO BOOT DIGEST SUMMARY")
    print(f"Repo: {os.path.basename(repo_root)}")
    stats = get_git_stats(repo_root)
    print(f"Commits: {stats['commits']}")
    print(f"Last: {stats['last_commit']}")
    print(f"Open PRs: {stats['open_prs_approx']}")
    print(f"Changed 7d: {stats['files_changed_7d']}")
    print(f"Report: {report_path}")
    print("STATUS: CONFIDENCE_OK")

if __name__ == "__main__":
    import sys
    fast_mode = '--fast' in sys.argv
    main(fast_mode)
