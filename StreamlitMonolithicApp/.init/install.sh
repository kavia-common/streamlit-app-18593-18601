#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
command -v python3 >/dev/null || { echo "python3 not found" >&2; exit 2; }
python3 -m pip --version >/dev/null || { echo "python3 pip not available" >&2; exit 3; }
# apt helper with small retries
apt_install_if_missing(){ pkg="$1"; if ! command -v nc >/dev/null && [ "$pkg" = "netcat-openbsd" ]; then :; fi; if ! dpkg -s "$pkg" >/dev/null 2>&1; then sudo apt-get update -qq || sleep 1; sudo apt-get install -y -qq "$pkg" || { sleep 2; sudo apt-get install -y "$pkg" || true; }; fi }
# install netcat-openbsd only if nc missing
if ! command -v nc >/dev/null; then apt_install_if_missing netcat-openbsd; fi
# write /etc/profile.d/streamlit_env.sh atomically with sudo to ensure ownership
sudo bash -c 'cat > /etc/profile.d/streamlit_env.sh <<"EOF"
# Streamlit environment variables (managed by setup script)
export PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
EOF
chmod 644 /etc/profile.d/streamlit_env.sh'
# export defaults into current shell safely
: "${PORT:=8501}"
: "${STREAMLIT_SERVER_HEADLESS:=true}"
export PORT STREAMLIT_SERVER_HEADLESS
# ensure workspace exists
mkdir -p "$WORKSPACE"
exit 0
