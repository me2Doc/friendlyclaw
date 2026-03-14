#!/bin/bash

# FriendlyClaw — Strategic Hive Control Script (v3.8.1)
# Professional CLI architecture with Robust Path Resolution.

# ── Dynamic Configuration ──────────────────────────────────
# Resolve the physical directory where the script is located (handle symlinks)
PHYSICAL_SCRIPT_PATH=$(readlink -f "${BASH_SOURCE[0]}")
INSTALL_DIR=$(dirname "$PHYSICAL_SCRIPT_PATH")
VENV_DIR="$INSTALL_DIR/venv"
ENV_FILE="$INSTALL_DIR/.env"
NODE_BIN="node"

# ── Colors ────────────────────────────────────────────────
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'

show_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "    __________  ___________   ______  ____  __   ________    ___ _       __"
    echo "   / ____/ __ \/  _/ ____/ | / / __ \/ /\ \/ /  / ____/ /   /   | |     / /"
    echo "  / /_  / /_/ // // __/ /  |/ / / / / /  \  /  / /   / /   / /| | | /| / / "
    echo " / __/ / _, _// // /___/ /|  / /_/ / /___/ /  / /___/ /___/ ___ | |/ |/ /  "
    echo "/_/   /_/ |_/___/_____/_/ |_/_____/_____/_/   \____/_____/_/  |_|__/|__/   "
    echo -e "${RESET}"
    echo -e "${BOLD}  FriendlyClaw — Strategic Hive Operative (v3.8.1)${RESET}"
    echo -e "${DIM}  Install Path: $INSTALL_DIR${RESET}"
    echo ""
}

show_help() {
    echo "Usage: friendlyclaw [options] [command]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Display help for command"
    echo "  -V, --version        Output the version number"
    echo ""
    echo "Commands:"
    echo "  start       Launch FriendlyClaw (Hatch TUI)"
    echo "  onboard     Run the High-Fidelity Onboarding (OpenClaw Style)"
    echo "  config *    Non-interactive config helpers (get/set/unset)"
    echo "  status      Show Hive health and active workers"
    echo "  memory *    Search and reindex SQLite-Vec memory"
    echo "  models *    Discover and configure LLM providers"
    echo "  security    Run a real-time security audit"
    echo "  logs        Show recent execution logs"
    echo "  update      Pull latest changes and update dependencies"
    echo "  uninstall   Remove local state and virtual environment"
}

check_node_deps() {
    if [ ! -d "$INSTALL_DIR/node_modules" ]; then
        echo -e "${YELLOW}📦 First run detected. Installing TUI dependencies...${RESET}"
        cd "$INSTALL_DIR"
        npm install --omit=optional -q
        echo -e "${GREEN}✅ Node dependencies ready.${RESET}"
    fi
}

onboard() {
    check_node_deps
    cd "$INSTALL_DIR"
    $NODE_BIN onboard.mjs
    return $?
}

start_app() {
    if [ ! -f "$ENV_FILE" ]; then
        onboard
        EXIT_CODE=$?
        [ $EXIT_CODE -ne 0 ] && exit 0
    fi

    # Virtual Environment check/init
    if [ ! -d "$VENV_DIR" ]; then
        echo "📦 Initializing virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    
    source "$VENV_DIR/bin/activate"
    
    # Python dependencies (quietly)
    pip install -q -r "$INSTALL_DIR/requirements.txt"

    echo -e "${GREEN}${BOLD}🚀 Launching Hive Brain...${RESET}"
    cd "$INSTALL_DIR"
    python3 main.py
}

run_python_cmd() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${RED}Error: Virtual environment not found. Run 'friendlyclaw onboard' first.${RESET}"
        exit 1
    fi
    source "$VENV_DIR/bin/activate"
    cd "$INSTALL_DIR"
    python3 main.py --cli "$@"
}

# ── Main Execution ────────────────────────────────────────

COMMAND=${1:-start}

case $COMMAND in
    start|tui)
        show_banner
        start_app
        ;;
    onboard|configure)
        onboard
        ;;
    config)
        shift
        run_python_cmd config "$@"
        ;;
    models|memory|status|cron|skills|security|doctor)
        run_python_cmd "$@"
        ;;
    logs)
        tail -f "$INSTALL_DIR/logs/brain.log" 2>/dev/null || tail -f "$INSTALL_DIR/logs/gateway.log" 2>/dev/null || echo "No logs found."
        ;;
    update)
        echo "🔄 Updating FriendlyClaw..."
        cd "$INSTALL_DIR"
        git pull
        source "$VENV_DIR/bin/activate"
        pip install -r requirements.txt
        echo -e "${GREEN}✅ Update complete.${RESET}"
        ;;
    uninstall)
        echo -e "${RED}${BOLD}⚠️  UNINSTALLING FRIENDLYCLAW STATE${RESET}"
        read -p "Are you sure? This will delete venv and .env [y/N]: " CONFIRM
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR" "$ENV_FILE" "$INSTALL_DIR/node_modules"
            echo -e "${GREEN}Cleanup complete.${RESET}"
        fi
        ;;
    version|-V)
        echo "FriendlyClaw v3.8.1-hive"
        ;;
    help|--help|-h)
        show_banner
        show_help
        ;;
    *)
        show_banner
        show_help
        exit 1
        ;;
esac
