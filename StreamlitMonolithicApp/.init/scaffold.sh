#!/usr/bin/env bash
set -euo pipefail
# Create workspace variable from container info
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
mkdir -p "$WORKSPACE" && cd "$WORKSPACE"
# create venv idempotently
if [ ! -d "$WORKSPACE/.venv" ]; then
  python3 -m venv "$WORKSPACE/.venv"
fi
VENV_PY="$WORKSPACE/.venv/bin/python"
[ -x "$VENV_PY" ] || { echo "venv python missing" >&2; exit 4; }
# upgrade pip inside venv (best-effort)
"$VENV_PY" -m pip install --disable-pip-version-check --no-cache-dir --upgrade pip setuptools wheel >/tmp/pip_upgrade.$$ 2>&1 || true
# write minimal requirements
cat > "$WORKSPACE"/requirements.txt <<'EOF'
streamlit>=1.20,<2
pytest
EOF
# minimal app
cat > "$WORKSPACE"/app.py <<'PY'
import os
import streamlit as st
port = int(os.environ.get('PORT', '8501'))
st.set_page_config(page_title='StreamlitMonolithicApp')
st.title('StreamlitMonolithicApp - Dev Scaffold')
st.write(f'Listening on port: {port}')
PY
# run script using venv python -m streamlit for robustness
cat > "$WORKSPACE"/run.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
[ -f /etc/profile.d/streamlit_env.sh ] && . /etc/profile.d/streamlit_env.sh || true
PORT=${PORT:-8501}
export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-true}
cd "$WORKSPACE"
exec "$WORKSPACE"/.venv/bin/python -m streamlit run "$WORKSPACE"/app.py --server.address 0.0.0.0 --server.port "$PORT"
SH
chmod +x "$WORKSPACE"/run.sh
# detect global streamlit for operator awareness (do not rely on it)
# write output to a predictable temp file for operator inspection
if python3 - <<'PY'
import pkgutil
try:
    if pkgutil.find_loader('streamlit'):
        import streamlit as s
        print('GLOBAL_STREAMLIT_VERSION=' + getattr(s, '__version__', 'unknown'))
except Exception:
    pass
PY
then
  true
fi > /tmp/global_streamlit.$$ 2>&1 || true
exit 0
