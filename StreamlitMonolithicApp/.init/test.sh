#!/usr/bin/env bash
set -euo pipefail
# testing-setup-and-smoke: install test helpers into venv, write pytest smoke test, run it
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
cd "$WORKSPACE"
VENV_PY="$WORKSPACE/.venv/bin/python"
[ -x "$VENV_PY" ] || { echo "venv python missing" >&2; exit 4; }
# install test helper libs into venv using unique tmp log
LOG_DEPS=/tmp/pip_test_deps.$$; "$VENV_PY" -m pip install --disable-pip-version-check --no-cache-dir requests pytest > "$LOG_DEPS" 2>&1 || { echo "failed installing test deps" >&2; tail -n 200 "$LOG_DEPS" >&2; rm -f "$LOG_DEPS"; exit 6; }
rm -f "$LOG_DEPS"
mkdir -p "$WORKSPACE"/tests
# write pytest smoke test
cat > "$WORKSPACE"/tests/test_smoke.py <<'PY'
import os, subprocess, time, signal, requests, sys
from pathlib import Path
PORT = int(os.environ.get('PORT', '8501'))
ROOT = Path(__file__).resolve().parent.parent
VENV_PY = str(ROOT / '.venv' / 'bin' / 'python')
# use python -m streamlit to avoid entrypoint edge-cases
cmd = [VENV_PY, '-m', 'streamlit', 'run', str(ROOT / 'app.py'), '--server.address', '0.0.0.0', '--server.port', str(PORT)]
# start in new process group so killpg will clean children
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
try:
    url = f'http://127.0.0.1:{PORT}/'
    deadline = time.time() + 45
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code in (200,301,302):
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        # dump small portion of stderr/stdout for debugging
        try:
            out, err = p.communicate(timeout=1)
            print(err.decode('utf-8', errors='ignore')[:200])
        except Exception:
            pass
        sys.exit(2)
finally:
    try:
        pgid = os.getpgid(p.pid)
        os.killpg(pgid, signal.SIGTERM)
    except Exception:
        try:
            p.terminate()
        except Exception:
            pass
    p.wait(timeout=5)
PY
# run pytest using venv pytest binary with minimal output
"$WORKSPACE"/.venv/bin/pytest -q "$WORKSPACE"/tests/test_smoke.py
RC=$?
exit $RC
