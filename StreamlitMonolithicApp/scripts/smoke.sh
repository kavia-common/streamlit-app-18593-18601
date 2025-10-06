#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
VENV_DIR="$WORKSPACE/.venv"
# load .env if present
if [ -f "$WORKSPACE/.env" ]; then set -a; . "$WORKSPACE/.env"; set +a; fi
PORT="${PORT:-8501}"
# prefer venv curl/commands; use curl to accept 200 or 3xx
TIMEOUT_BIN=$(command -v timeout || true)
check_http() {
  http_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/" 2>/dev/null || true)
  case "$http_status" in
    200|301|302|303|307|308) return 0 ;;
    *) return 1 ;;
  esac
}
if [ -n "$TIMEOUT_BIN" ]; then
  $TIMEOUT_BIN 30 bash -c 'until check_http; do sleep 0.5; done' || (echo 'smoke: http probe failed' >&2; exit 2)
else
  SECS=0
  until check_http || [ $SECS -ge 30 ]; do sleep 0.5; SECS=$((SECS+1)); done
  if [ $SECS -ge 30 ]; then echo 'smoke: http probe failed' >&2; exit 2; fi
fi
echo OK
