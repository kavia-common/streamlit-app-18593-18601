#!/usr/bin/env bash
set -euo pipefail

# Validation script for Streamlit (validation-run)
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
cd "$WORKSPACE"
VENV_DIR="$WORKSPACE/.venv"
if [ ! -x "$VENV_DIR/bin/python" ]; then echo 'venv missing, run deps-001' >&2; exit 2; fi
# load workspace .env if present (authoritative)
if [ -f "$WORKSPACE/.env" ]; then set -a; . "$WORKSPACE/.env"; set +a; fi
PORT="${PORT:-8501}"
VALIDATION_TIMEOUT="${VALIDATION_TIMEOUT:-30}"
LOGFILE="$WORKSPACE/streamlit_validation.log"
PIDFILE="$WORKSPACE/streamlit_validation.pid"

# ensure streamlit binary exists in venv
if [ ! -x "$VENV_DIR/bin/streamlit" ]; then echo 'streamlit not installed in venv, run deps-001' >&2; exit 3; fi

# start Streamlit in its own session/process-group using setsid; redirect output to logfile
: >"$LOGFILE"  # truncate or create
setsid "$VENV_DIR/bin/streamlit" run "$WORKSPACE/app.py" --server.headless true --server.port "$PORT" >"$LOGFILE" 2>&1 &
PID=$!
# persist PID
echo "$PID" > "$PIDFILE"
# derive PGID robustly from PID
PGID=$(ps -o pgid= "$PID" 2>/dev/null | tr -d ' ' || true)
# fallback: if pgid empty or 0, use PID (still safe guard below)
if [ -z "$PGID" ] || [ "$PGID" = "0" ]; then PGID="$PID"; fi

# readiness: prefer HTTP 200/3xx, else fallback to scanning logfile for keywords
READY=1
SECS=0
while [ $SECS -lt "$VALIDATION_TIMEOUT" ]; do
  http_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/" 2>/dev/null || true)
  case "$http_status" in
    200|301|302|303|307|308)
      READY=0; break;;
  esac
  if grep -E -i "(Running on|Server should start|HTTP server|Server running|You can now view)" "$LOGFILE" >/dev/null 2>&1; then READY=0; break; fi
  sleep 1
  SECS=$((SECS+1))
done

if [ $READY -ne 0 ]; then
  echo "Streamlit did not become ready within ${VALIDATION_TIMEOUT}s. See $LOGFILE" >&2
  # attempt graceful termination of the group if PGID looks numeric and non-zero
  if [[ "$PGID" =~ ^[0-9]+$ ]] && [ "$PGID" != "0" ]; then
    kill -- -"$PGID" 2>/dev/null || true
    sleep 2
    kill -9 -- -"$PGID" 2>/dev/null || true
  else
    # fallback: try killing the direct PID
    kill "$PID" 2>/dev/null || true
    sleep 1
    kill -9 "$PID" 2>/dev/null || true
  fi
  exit 4
fi

# run smoke script (must be executable at scripts/smoke.sh)
if [ -x "scripts/smoke.sh" ]; then
  if scripts/smoke.sh; then echo "Validation: smoke test passed"; else
    echo "Validation: smoke test failed" >&2
    if [[ "$PGID" =~ ^[0-9]+$ ]] && [ "$PGID" != "0" ]; then
      kill -- -"$PGID" 2>/dev/null || true; sleep 2; kill -9 -- -"$PGID" 2>/dev/null || true
    else
      kill "$PID" 2>/dev/null || true; sleep 1; kill -9 "$PID" 2>/dev/null || true
    fi
    exit 5
  fi
else
  echo "scripts/smoke.sh missing or not executable; failing validation" >&2
  # cleanup
  if [[ "$PGID" =~ ^[0-9]+$ ]] && [ "$PGID" != "0" ]; then
    kill -- -"$PGID" 2>/dev/null || true; sleep 2; kill -9 -- -"$PGID" 2>/dev/null || true
  else
    kill "$PID" 2>/dev/null || true; sleep 1; kill -9 "$PID" 2>/dev/null || true
  fi
  exit 6
fi

# stop server gracefully using PGID where safe
if [[ "$PGID" =~ ^[0-9]+$ ]] && [ "$PGID" != "0" ]; then
  kill -- -"$PGID" 2>/dev/null || true
else
  kill "$PID" 2>/dev/null || true
fi

# wait up to 5s for termination
for i in 1 2 3 4 5; do
  if ! kill -0 "$PID" 2>/dev/null; then break; fi
  sleep 1
done
# final escalate to SIGKILL if still alive
if kill -0 "$PID" 2>/dev/null; then
  if [[ "$PGID" =~ ^[0-9]+$ ]] && [ "$PGID" != "0" ]; then
    kill -9 -- -"$PGID" 2>/dev/null || true
  else
    kill -9 "$PID" 2>/dev/null || true
  fi
fi

# Evidence
echo "Validation succeeded. Log excerpt:" || true
tail -n 50 "$LOGFILE" || true
# cleanup PID file
rm -f "$PIDFILE" || true

exit 0
