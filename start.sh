#!/usr/bin/env bash
# One-command setup + launch for Project Double Double.
# Installs Python 3.12+ and Node 20.19+ if missing, sets up a venv and node_modules,
# then runs the FastAPI backend (:8000) and the Vite frontend (:5173).
#
#   ./start.sh               install whatever is missing, then start both servers
#   ./start.sh --setup-only  install only, don't start anything
#
# Works on macOS, Linux (apt/dnf/pacman/zypper) and Windows via Git Bash / WSL.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV_DIR:-$ROOT/.venv}"
REQS="$ROOT/backend/app/requirements.txt"
SETUP_ONLY=0
[ "${1:-}" = "--setup-only" ] && SETUP_ONLY=1

PY_MIN="3.12"
NODE_MIN_MAJOR=20
NODE_MIN_MINOR=19   # Vite 8 needs Node 20.19+ (or 22.12+)
NVM_VERSION="v0.40.3"

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m  %s\n' "$*" >&2; }
die()  { printf '\033[1;31mxx\033[0m  %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

SUDO=""
if [ "$(id -u)" -ne 0 ] && have sudo; then SUDO="sudo"; fi

# Which system package manager do we have?
detect_pm() {
  if   have brew;    then echo brew
  elif have apt-get; then echo apt
  elif have dnf;     then echo dnf
  elif have pacman;  then echo pacman
  elif have zypper;  then echo zypper
  elif have winget;  then echo winget
  else echo none
  fi
}
PM="$(detect_pm)"

pm_install() { # pm_install <brew pkgs> | <apt pkgs> | <dnf pkgs> | <pacman pkgs> | <zypper pkgs>
  local brew_p apt_p dnf_p pac_p zyp_p
  IFS='|' read -r brew_p apt_p dnf_p pac_p zyp_p <<<"$1"
  case "$PM" in
    brew)   brew install $brew_p ;;
    apt)    $SUDO apt-get update -y && $SUDO apt-get install -y $apt_p ;;
    dnf)    $SUDO dnf install -y $dnf_p ;;
    pacman) $SUDO pacman -Sy --noconfirm $pac_p ;;
    zypper) $SUDO zypper install -y $zyp_p ;;
    *)      return 1 ;;
  esac
}

# ---------- Python ----------
py_ok() { "$1" -c "import sys; sys.exit(0 if sys.version_info >= (${PY_MIN/./,}) else 1)" >/dev/null 2>&1; }

find_python() {
  local c
  for c in python3.14 python3.13 python3.12 python3 python py; do
    if have "$c" && py_ok "$c"; then echo "$c"; return 0; fi
  done
  return 1
}

PYTHON="$(find_python || true)"
if [ -z "$PYTHON" ]; then
  log "Python $PY_MIN+ not found, installing"
  if [ "$PM" = winget ]; then
    winget install -e --id Python.Python.3.12
    die "Python installed. Open a new terminal (so PATH refreshes) and re-run ./start.sh"
  fi
  pm_install "python@3.12|python3 python3-venv python3-pip|python3 python3-pip|python python-pip|python3 python3-pip" \
    || die "No supported package manager. Install Python $PY_MIN+ from https://www.python.org/downloads/ and re-run."
  PYTHON="$(find_python || true)"
  [ -n "$PYTHON" ] || die "Python $PY_MIN+ still not found after install (distro may ship an older one). Install it manually and re-run."
fi
log "Using $($PYTHON --version) ($(command -v "$PYTHON"))"

# ---------- Node ----------
node_ok() {
  have node && have npm || return 1
  local v major minor
  v="$(node -v | sed 's/^v//')"; major="${v%%.*}"; minor="${v#*.}"; minor="${minor%%.*}"
  if [ "$major" -gt "$NODE_MIN_MAJOR" ]; then return 0; fi
  [ "$major" -eq "$NODE_MIN_MAJOR" ] && [ "$minor" -ge "$NODE_MIN_MINOR" ]
}

install_node_nvm() {
  have curl || die "curl is needed to install Node via nvm. Install curl or Node $NODE_MIN_MAJOR.$NODE_MIN_MINOR+ and re-run."
  export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    log "Installing nvm $NVM_VERSION"
    curl -fsSL "https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VERSION/install.sh" | PROFILE=/dev/null bash
  fi
  # nvm.sh isn't safe under `set -eu`
  set +eu
  # shellcheck disable=SC1091
  . "$NVM_DIR/nvm.sh"
  nvm install --lts && nvm use --lts
  set -eu
}

if ! node_ok; then
  log "Node $NODE_MIN_MAJOR.$NODE_MIN_MINOR+ not found, installing"
  case "$PM" in
    brew)   brew install node ;;
    dnf)    $SUDO dnf install -y nodejs npm ;;
    pacman) $SUDO pacman -Sy --noconfirm nodejs npm ;;
    zypper) $SUDO zypper install -y nodejs npm ;;
    winget) winget install -e --id OpenJS.NodeJS.LTS
            die "Node installed. Open a new terminal (so PATH refreshes) and re-run ./start.sh" ;;
    *)      : ;;   # apt ships an old Node, so use nvm
  esac
  node_ok || install_node_nvm
  node_ok || die "Node $NODE_MIN_MAJOR.$NODE_MIN_MINOR+ still not available. Install it from https://nodejs.org and re-run."
fi
log "Using node $(node -v), npm $(npm -v)"

# ---------- Backend deps ----------
if [ ! -x "$VENV/bin/python" ] && [ ! -x "$VENV/Scripts/python.exe" ]; then
  log "Creating virtual environment at $VENV"
  "$PYTHON" -m venv "$VENV" || die "venv creation failed. On Debian/Ubuntu run: sudo apt install python3-venv"
fi
if   [ -x "$VENV/bin/python" ];         then VPY="$VENV/bin/python"
else                                         VPY="$VENV/Scripts/python.exe"
fi

# Reinstall only when requirements.txt changed.
STAMP="$VENV/.requirements.sum"
SUM="$(cksum <"$REQS" | cut -d' ' -f1,2)"
if [ ! -f "$STAMP" ] || [ "$(cat "$STAMP")" != "$SUM" ]; then
  log "Installing backend dependencies"
  "$VPY" -m pip install --quiet --upgrade pip
  "$VPY" -m pip install -r "$REQS"
  echo "$SUM" >"$STAMP"
else
  log "Backend dependencies up to date"
fi

# ---------- Frontend deps ----------
log "Installing frontend dependencies"
(cd "$ROOT/frontend" && npm install --no-audit --no-fund)

if [ "$SETUP_ONLY" -eq 1 ]; then
  log "Setup complete. Run ./start.sh to launch."
  exit 0
fi

# ---------- Run ----------
for port in 8000 5173; do
  if (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
    die "Port $port is already in use. Stop whatever is using it and re-run."
  fi
done

PIDS=()
cleanup() {
  trap - EXIT
  echo
  log "Shutting down"
  local p
  for p in "${PIDS[@]:-}"; do
    [ -n "$p" ] || continue
    pkill -P "$p" 2>/dev/null || true   # uvicorn reloader / vite child
    kill "$p" 2>/dev/null || true
  done
  wait 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT TERM

log "Backend  -> http://127.0.0.1:8000  (docs at /docs)"
# Must run from backend/ because the data path is relative (data/restaurants.json).
(cd "$ROOT/backend" && exec "$VPY" -m uvicorn app.main:app --reload) &
PIDS+=($!)

log "Frontend -> http://localhost:5173"
(cd "$ROOT/frontend" && exec npm run dev) &
PIDS+=($!)

log "Press Ctrl+C to stop both."
# macOS ships bash 3.2 (no `wait -n`), so poll: stop everything if either server dies.
while :; do
  for p in "${PIDS[@]}"; do
    kill -0 "$p" 2>/dev/null || { warn "A server exited, stopping the other."; exit 1; }
  done
  sleep 1
done
