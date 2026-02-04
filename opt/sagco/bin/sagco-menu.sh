#!/bin/bash
set -euo pipefail

PY="${SAGCO_BIN:-/opt/sagco/bin}/sagco-menu.py"
SPM="${SPM_PATH:-/opt/sagco/spm.yml}"
export SPM_PATH="$SPM"

# Only run in interactive TTY
if [[ ! -t 0 ]]; then exit 0; fi
if [[ ! -f "$SPM" ]]; then
  echo "SAGCO: missing $SPM"
  exit 1
fi

while true; do
  # Recent as special category if exists
  RECENT_ARGS=()
  while IFS=$'\t' read -r name icon desc cmd cat_key; do
    [[ -z "$name" ]] && continue
    RECENT_ARGS+=("$name" "${icon:+ $icon }${desc:-$name}")
  done < <("$PY" recent)
  if [[ ${#RECENT_ARGS[@]} -gt 0 ]]; then
    MENU_ARGS=("recent" "🕒 Recently Used")
  else
    MENU_ARGS=()
  fi

  # Build category menu (ordered + icons)
  while IFS=$'\t' read -r key icon d; do
    [[ -z "$key" ]] && continue
    MENU_ARGS+=("$key" "${icon:+ $icon }${d:-$key}")
  done < <("$PY" categories)

  CHOICE=$(whiptail --title "SAGCO Tools Menu" --menu "Select category:" 20 78 12 \
    "${MENU_ARGS[@]}" 3>&1 1>&2 2>&3) || exit 0

  # Search prompt (global if non-empty)
  SEARCH=$(whiptail --title "Search $CHOICE" --inputbox "Enter search term (optional):" 8 78 "" 3>&1 1>&2 2>&3) || continue
  EFFECTIVE_CHOICE="$CHOICE"
  if [[ -n "$SEARCH" ]]; then
    EFFECTIVE_CHOICE="all"  # Global search
  fi

  # Build tool menu (with icons + search)
  TOOL_ARGS=()
  declare -A CMD_MAP=()
  declare -A CAT_MAP=()
  while IFS=$'\t' read -r name icon desc cmd cat_key; do
    [[ -z "$name" || -z "$cmd" ]] && continue
    TOOL_ARGS+=("$name" "${icon:+ $icon }${desc:-$name}")
    CMD_MAP["$name"]="$cmd"
    CAT_MAP["$name"]="$cat_key"
  done < <("$PY" items "$EFFECTIVE_CHOICE" "$SEARCH")

  if [[ ${#TOOL_ARGS[@]} -eq 0 ]]; then
    whiptail --title "No Results" --msgbox "No tools matched your search." 8 50
    continue
  fi

  TOOL=$(whiptail --title "SAGCO: $CHOICE" --menu "Select tool:" 22 90 12 \
    "${TOOL_ARGS[@]}" 3>&1 1>&2 2>&3) || continue

  CMD="${CMD_MAP[$TOOL]}"
  CAT_KEY="${CAT_MAP[$TOOL]}"
  clear
  echo "SAGCO ▶ $TOOL"
  echo "CMD  ▶ $CMD"
  echo
  bash -lc "$CMD"
  echo
  "$PY" add_recent "$CAT_KEY" "$TOOL"  # Add to recent with cat_key
  read -r -p "Press Enter to return to menu..."
done
