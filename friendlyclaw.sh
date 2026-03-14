#!/bin/bash

# FriendlyClaw — Strategic Hive Control Script (v3.5)
# Professional CLI architecture mirroring OpenClaw commands.

# Configuration
INSTALL_DIR="/home/me2doc/friendlyclaw"
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

show_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "    __________  ___________   ______  ____  __   ________    ___ _       __"
    echo "   / ____/ __ \/  _/ ____/ | / / __ \/ /\ \/ /  / ____/ /   /   | |     / /"
    echo "  / /_  / /_/ // // __/ /  |/ / / / / /  \  /  / /   / /   / /| | | /| / / "
    echo " / __/ / _, _// // /___/ /|  / /_/ / /___/ /  / /___/ /___/ ___ | |/ |/ /  "
    echo "/_/   /_/ |_/___/_____/_/ |_/_____/_____/_/   \____/_____/_/  |_|__/|__/   "
    echo -e "${RESET}"
    echo -e "${BOLD}  FriendlyClaw — Strategic Hive Operative (v3.5.0)${RESET}"
    echo -e "${DIM}  Your .env is showing; don't worry, I'll pretend I didn't see it.${RESET}"
    echo ""
}

show_help() {
    echo "Usage: friendlyclaw [options] [command]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Display help for command"
    echo "  -V, --version        Output the version number"
    echo "  --no-color           Disable ANSI colors"
    echo ""
    echo "Commands:"
    echo "  Hint: commands suffixed with * have subcommands. Run <command> --help for details."
    echo "  agent                Run one agent turn via the CLI"
    echo "  config *             Non-interactive config helpers (get/set/unset/file)"
    echo "  configure            Interactive setup wizard for credentials and platform"
    echo "  cron *               Manage scheduled missions (Heartbeat/Cron)"
    echo "  dashboard            Open the World Monitor (Port 5173)"
    echo "  doctor               Health checks for the Brain & Body"
    echo "  logs                 Tail brain file logs"
    echo "  memory *             Search and reindex SQLite-Vec memory"
    echo "  models *             Discover and configure LLM providers"
    echo "  onboard              Full interactive onboarding wizard (TUI)"
    echo "  security *           Security tools and local config audits"
    echo "  skills *             List and inspect available Hive skills"
    echo "  status               Show Hive health and active workers"
    echo "  tui                  Open a terminal UI connected to the Brain"
    echo "  update *             Update FriendlyClaw and dependencies"
    echo "  uninstall            Remove state and virtual environment"
    echo ""
    echo "Examples:"
    echo "  friendlyclaw models list"
    echo "  friendlyclaw memory search \"Project Lucy\""
    echo "  friendlyclaw onboard"
}

run_python_cmd() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${RED}Error: Virtual environment not found. Run 'friendlyclaw onboard' first.${RESET}"
        exit 1
    fi
    source "$VENV_DIR/bin/activate"
    cd "$INSTALL_DIR"
    # Execute a specific Python entrypoint for CLI commands
    python3 main.py --cli "$@"
}

# ── Main Execution ────────────────────────────────────────

COMMAND=${1:-start}

case $COMMAND in
    start|tui)
        show_banner
        # Standard launch
        if [ ! -f "$ENV_FILE" ]; then
            $NODE_BIN onboard.mjs
            [ $? -ne 0 ] && exit 0
        fi
        source "$VENV_DIR/bin/activate"
        cd "$INSTALL_DIR"
        python3 main.py
        ;;
    onboard|configure)
        show_banner
        cd "$INSTALL_DIR"
        $NODE_BIN onboard.mjs
        ;;
    config)
        shift
        # Implement config logic...
        ;;
    models|memory|status|cron|skills|security|doctor)
        run_python_cmd "$@"
        ;;
    logs)
        tail -f "$INSTALL_DIR/logs/brain.log" 2>/dev/null || echo "No logs found."
        ;;
    update)
        echo "🔄 Updating FriendlyClaw..."
        git pull
        source "$VENV_DIR/bin/activate"
        pip install -r requirements.txt
        echo -e "${GREEN}✅ Update complete.${RESET}"
        ;;
    uninstall)
        echo -e "${RED}${BOLD}⚠️  UNINSTALLING FRIENDLYCLAW STATE${RESET}"
        read -p "Are you sure? This will delete venv and .env [y/N]: " CONFIRM
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR" "$ENV_FILE"
            echo -e "${GREEN}Cleanup complete.${RESET}"
        fi
        ;;
    version|-V)
        echo "FriendlyClaw v3.5.0-hive"
        ;;
    help|--help|-h)
        show_banner
        show_help
        ;;
    *)
        # Default to showing help if unknown
        show_banner
        show_help
        exit 1
        ;;
esac
