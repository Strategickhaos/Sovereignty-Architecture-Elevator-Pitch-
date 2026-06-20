import json, subprocess
from pathlib import Path

def scan(output_dir: Path) -> list[dict]:
    results = []
    try:
        raw = subprocess.check_output(
            ["docker", "ps", "--format", "{{json .}}"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode()
        for line in raw.strip().splitlines():
            if line:
                results.append(json.loads(line))
    except Exception as e:
        results.append({"error": str(e), "note": "docker not running or not installed"})

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "docker.json"
    out.write_text(json.dumps(results, indent=2))
    container_count = sum(1 for r in results if "error" not in r)
    print(f"  docker    → {container_count} container(s)  [{out}]")
    return results
