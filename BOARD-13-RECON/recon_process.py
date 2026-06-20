import json, os, platform
from pathlib import Path

def scan(output_dir: Path) -> list[dict]:
    results = []
    try:
        import psutil
        for p in psutil.process_iter(["pid", "name", "status", "cpu_percent", "create_time"]):
            try:
                results.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except ImportError:
        # fallback: read /proc on Linux
        if platform.system() == "Linux":
            for pid_dir in Path("/proc").iterdir():
                if pid_dir.name.isdigit():
                    try:
                        name = (pid_dir / "comm").read_text().strip()
                        results.append({"pid": int(pid_dir.name), "name": name, "status": "unknown"})
                    except Exception:
                        pass

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "processes.json"
    out.write_text(json.dumps(results, default=str, indent=2))
    print(f"  processes → {len(results)} found  [{out}]")
    return results
