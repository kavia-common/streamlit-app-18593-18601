#!/usr/bin/env bash
set -euo pipefail
# validation-build-run-stop
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
cd "$WORKSPACE"
[ -f /etc/profile.d/streamlit_env.sh ] && . /etc/profile.d/streamlit_env.sh || true
PORT=${PORT:-8501}
VENV_PY="$WORKSPACE/.venv/bin/python"
if [ ! -x "$VENV_PY" ]; then echo "venv python missing, run deps step" >&2; exit 4; fi
LOG_OUT="/tmp/streamlit.out.$$"; LOG_ERR="/tmp/streamlit.err.$$"
# start server in background in its own session
setsid "$VENV_PY" -m streamlit run "$WORKSPACE"/app.py --server.address 0.0.0.0 --server.port "$PORT" >"$LOG_OUT" 2>"$LOG_ERR" &
LAUNCH_PID=$!
# give short time for process to spawn
sleep 1
# try to get PGID robustly
PGID=""
if ps -o pgid= -p "$LAUNCH_PID" >/dev/null 2>&1; then
  PGID=$(ps -o pgid= -p "$LAUNCH_PID" | tr -d ' ')
fi
if [ -z "$PGID" ]; then
  STREAM_PID=$(pgrep -f "-m streamlit run .*app.py" | head -n1 || true)
  if [ -n "$STREAM_PID" ]; then
    PGID=$(ps -o pgid= -p "$STREAM_PID" | tr -d ' ') || PGID=""
  fi
fi
# readiness probe
URL="http://127.0.0.1:$PORT/"
READY=0; RETRIES=45; SLEEP=1
for i in $(seq 1 $RETRIES); do
  if curl -sS --max-time 5 -I "$URL" >/dev/null 2>&1; then READY=1; break; fi
  if command -v nc >/dev/null 2>&1 && nc -z 127.0.0.1 "$PORT" >/dev/null 2>&1; then READY=1; break; fi
  sleep $SLEEP
done
if [ "$READY" -ne 1 ]; then
  echo "server not ready after timeout" >&2
  echo "--- last stdout (tail 200) ---" >&2; tail -n 200 "$LOG_OUT" >&2 || true
  echo "--- last stderr (tail 200) ---" >&2; tail -n 200 "$LOG_ERR" >&2 || true
  if [ -n "$PGID" ]; then kill -TERM -"$PGID" >/dev/null 2>&1 || true; fi
  wait "$LAUNCH_PID" 2>/dev/null || true
  exit 7
fi
# fetch root and show minimal evidence
RESP_FILE="/tmp/streamlit_resp.$$"
HTTP_STATUS=$(curl -sS -o "$RESP_FILE" -w "%{http_code}" "$URL" || true)
if [ -z "$HTTP_STATUS" ]; then
  echo "no HTTP response" >&2
  if [ -n "$PGID" ]; then kill -TERM -"$PGID" >/dev/null 2>&1 || true; fi
  exit 8
fi
# print minimal evidence: first 200 bytes and HTTP status
head -c 200 "$RESP_FILE" || true
echo "\nHTTP_STATUS:$HTTP_STATUS"
# stop app cleanly (entire process group if available)
if [ -n "$PGID" ]; then
  kill -TERM -"$PGID" >/dev/null 2>&1 || true
else
  kill -TERM "$LAUNCH_PID" >/dev/null 2>&1 || true
fi
wait "$LAUNCH_PID" 2>/dev/null || true
exit 0
