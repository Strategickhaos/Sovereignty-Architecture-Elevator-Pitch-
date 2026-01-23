#!/usr/bin/env python3
import argparse, json, subprocess, time, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def run_action(action, params):
    if action == "baseline":
        return
    elif action == "vpn_down":
        subprocess.run([str(ROOT / "injectors/vpn_toggle.sh"), "down"], check=True)
    elif action == "vpn_up":
        subprocess.run([str(ROOT / "injectors/vpn_toggle.sh"), "up"], check=True)
    elif action == "latency_set":
        ms = str(params["ms"])
        subprocess.run([str(ROOT / "injectors/netem.sh"), "set", ms], check=True)
    elif action == "latency_clear":
        subprocess.run([str(ROOT / "injectors/netem.sh"), "clear"], check=True)
    else:
        raise ValueError(f"unknown action {action}")

def load_scenario(path):
    with open(path) as f:
        return json.loads(json.dumps(__import__("yaml").safe_load(f)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario", help="scenario YAML")
    args = ap.parse_args()

    scenario = load_scenario(args.scenario)
    duration = scenario["duration_s"]
    timeline = sorted(scenario["timeline"], key=lambda e: e["t"])

    start = time.time()
    next_idx = 0

    print(json.dumps({"event": "scenario_start", "ts": now_iso(), "id": scenario["id"]}))
    while True:
        now = time.time()
        elapsed = now - start

        # trigger actions
        while next_idx < len(timeline) and elapsed >= timeline[next_idx]["t"]:
            evt = timeline[next_idx]
            run_action(evt["action"], evt.get("params", {}))
            print(json.dumps({
                "event": "action",
                "ts": now_iso(),
                "action": evt["action"],
                "params": evt.get("params", {})
            }))
            next_idx += 1

        if elapsed >= duration:
            break

        time.sleep(0.1)

    print(json.dumps({"event": "scenario_end", "ts": now_iso()}))

if __name__ == "__main__":
    main()
