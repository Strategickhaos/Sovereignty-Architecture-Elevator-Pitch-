#!/usr/bin/env bash
# watch_harbor.sh
# Air-gapped drift monitor: detects changes, diffs, re-embeds SHA256, re-signs with GPG
# No network. No external binaries. Runs forever in restricted environments.

set -euo pipefail
IFS=$'\n\t'

# === CONFIGURATION ===
LOCAL="${LOCAL:-./dao_record.yaml}"
REF="${REF:-./harbor_profile.yaml}"
SIG="${SIG:-${LOCAL}.asc}"
GPG_ID="${GPG_ID:-}"
INTERVAL="${INTERVAL:-5}"
DIFF_OUT="${DIFF_OUT:-./dao_diff.patch}"
LOG="${LOG:-./watch_harbor.log}"

# === DEPENDENCY CHECK ===
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }; }
need sha256sum
need gpg
need diff

# === INPUT VALIDATION ===
[[ -z "$GPG_ID" ]] && { echo "Set GPG_ID (e.g., export GPG_ID='domenic.garza@snhu.edu')"; exit 1; }
[[ ! -f "$LOCAL" ]] && { echo "Missing local file: $LOCAL"; exit 1; }
[[ ! -f "$REF" ]] && { echo "Missing reference file: $REF (export from Harbor Compliance offline)"; exit 1; }

# === INITIAL STATE ===
last_hash=""
echo "[WATCHER START] $(date -u +'%Y-%m-%dT%H:%M:%SZ')" | tee -a "$LOG"
echo "→ Monitoring: $LOCAL ↔ $REF" | tee -a "$LOG"
echo "→ Interval: ${INTERVAL}s | Diff: $DIFF_OUT | Sig: $SIG" | tee -a "$LOG"

# === MAIN LOOP ===
while true; do
  cur_hash="$( { sha256sum "$LOCAL" "$REF" 2>/dev/null || true; } | sha256sum | awk '{print $1}')"
  
  if [[ "$cur_hash" != "$last_hash" ]]; then
    TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
    echo "CHANGE DETECTED @ $TS" | tee -a "$LOG"

    # 1. Generate unified diff
    if diff -u "$REF" "$LOCAL" > "$DIFF_OUT" 2>/dev/null; then
      echo "  • No drift (files identical)" | tee -a "$LOG"
      > "$DIFF_OUT"  # clear patch if no changes
    else
      echo "  • Drift detected → $DIFF_OUT" | tee -a "$LOG"
      echo "    $(wc -l < "$DIFF_OUT") lines changed" | tee -a "$LOG"
    fi

    # 2. Re-embed SHA256 into LOCAL
    sum_local="$(sha256sum "$LOCAL" | awk '{print $1}')"
    if command -v yq >/dev/null 2>&1; then
      tmp="$(mktemp)"
      yq e ".generated.checksums.sha256 = \"$sum_local\"" "$LOCAL" > "$tmp" && mv "$tmp" "$LOCAL"
    else
      tmp="$(mktemp)"
      awk -v sum="$sum_local" '
        BEGIN { in_gen=0; printed=0 }
        /^generated:/ { in_gen=1; print; print "  checksums:\n    sha256: \"" sum "\""; printed=1; next }
        in_gen && /^  [a-z]/ && !printed { print "  checksums:\n    sha256: \"" sum "\""; printed=1 }
        { print }
      ' "$LOCAL" > "$tmp" && mv "$tmp" "$LOCAL"
    fi

    # 3. Re-sign with GPG
    if [[ -n "$GPG_ID" ]]; then
      gpg --armor --local-user "$GPG_ID" --output "$SIG" --detach-sign "$LOCAL" 2>/dev/null
      if gpg --verify "$SIG" "$LOCAL" >/dev/null 2>&1; then
        echo "  • Signature VALID → $SIG" | tee -a "$LOG"
      else
        echo "  • SIGNATURE FAILED" | tee -a "$LOG" >&2
        exit 1
      fi
    fi

    # 4. Final audit line
    echo "  • SHA256: $sum_local" | tee -a "$LOG"
    echo "  • Updated: $LOCAL, $SIG, $DIFF_OUT" | tee -a "$LOG"
    echo "────────────────────────────────" | tee -a "$LOG"

    last_hash="$cur_hash"
  fi

  sleep "$INTERVAL"
done