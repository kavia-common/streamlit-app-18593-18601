#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
cd "$WORKSPACE"
VENV_DIR="$WORKSPACE/.venv"
PIP_LOG="$WORKSPACE/venv_install.log"
# create venv idempotently
if [ ! -d "$VENV_DIR" ]; then python3 -m venv "$VENV_DIR"; fi
# record venv python and pip versions
"$VENV_DIR/bin/python" --version 2>&1 | tee -a "$PIP_LOG" || true
"$VENV_DIR/bin/pip" --version 2>&1 | tee -a "$PIP_LOG" || true
# helper: retry cmd up to 3 times with backoff
_retry() { local n=0; local max=3; local delay=2; until "$@"; do n=$((n+1)); if [ $n -ge $max ]; then return 1; fi; sleep $((delay * n)); done }
# upgrade pip tooling
_retry "$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel >>"$PIP_LOG" 2>&1 || (cat "$PIP_LOG" && exit 4)
# install requirements if present (retry on transient network errors)
if [ -f requirements.txt ]; then _retry "$VENV_DIR/bin/python" -m pip install -r requirements.txt >>"$PIP_LOG" 2>&1 || (cat "$PIP_LOG" && exit 5); fi
# log streamlit version if available
if [ -x "$VENV_DIR/bin/streamlit" ]; then "$VENV_DIR/bin/streamlit" --version >>"$PIP_LOG" 2>&1 || true; fi
# Write guarded profile drop for interactive shells (idempotent)
PROFILE=/etc/profile.d/streamlit_venv.sh
TMP=$(mktemp)
cat > "$TMP" <<'EOF'
# created by StreamlitMonolithicApp setup - prepend workspace venv bin for interactive shells
if [ -d "${VENV_DIR}/bin" ]; then
  case ":$PATH:" in
    *":${VENV_DIR}/bin:"*) ;;
    *) export PATH="${VENV_DIR}/bin:$PATH" ;;
  esac
fi
EOF
if ! sudo test -f "$PROFILE" || ! sudo cmp -s "$TMP" "$PROFILE" 2>/dev/null; then sudo cp "$TMP" "$PROFILE" && sudo chmod 644 "$PROFILE"; fi
rm -f "$TMP"
# print tail of log for evidence
tail -n 50 "$PIP_LOG" || true
