#!/bin/bash

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${CYAN}${BOLD}"
echo "    __________  ___________   ______  ____  __   ________    ___ _       __"
echo "   / ____/ __ \/  _/ ____/ | / / __ \/ /\ \/ /  / ____/ /   /   | |     / /"
echo "  / /_  / /_/ // // __/ /  |/ / / / / /  \  /  / /   / /   / /| | | /| / / "
echo " / __/ / _, _// // /___/ /|  / /_/ / /___/ /  / /___/ /___/ ___ | |/ |/ /  "
echo "/_/   /_/ |_/___/_____/_/ |_/_____/_____/_/   \____/_____/_/  |_|__/|__/   "
echo -e "${RESET}"
echo -e "${BOLD}  FriendlyClaw — Autonomous AI Operator (Body: OpenClaw)${RESET}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Python check ──────────────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found.${RESET}"
    echo "Install it: https://python.org"
    exit 1
fi

# Check Python version (>= 3.10)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
    echo -e "${RED}❌ Python version 3.10+ required (found $PYTHON_VERSION).${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ Python: $PYTHON_VERSION${RESET}"

# ── Node.js check ──────────────────────────────────────────
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found.${RESET}"
    echo "Install it (v22+ required): https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
if [ "$NODE_MAJOR" -lt 22 ]; then
    echo -e "${RED}❌ Node.js v22+ required (found v$NODE_VERSION).${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js: v$NODE_VERSION${RESET}"

# ── Virtual environment ───────────────────────────────────
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment active${RESET}"

# ── Install dependencies ──────────────────────────────────
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${RESET}"

# ── .env setup ────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  Setup${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""

    # Platform
    echo -e "${YELLOW}Platform:${RESET}"
    echo "  1) Telegram"
    echo "  2) CLI (terminal)"
    read -p "  Choose [1/2]: " PLATFORM_CHOICE

    if [ "$PLATFORM_CHOICE" = "1" ]; then
        sed -i "s/PLATFORM=cli/PLATFORM=telegram/" .env
        echo ""
        echo -e "${YELLOW}Telegram Bot Token${RESET}"
        echo "  Get it from @BotFather on Telegram"
        read -p "  Token: " BOT_TOKEN
        sed -i "s/your_telegram_bot_token_here/$BOT_TOKEN/" .env
    else
        sed -i "s/PLATFORM=telegram/PLATFORM=cli/" .env
    fi

    # Model provider
    echo ""
    echo -e "${YELLOW}Model Provider:${RESET}"
    echo "  1) Gemini (free — recommended)"
    echo "  2) OpenAI"
    echo "  3) OpenRouter (100+ models)"
    echo "  4) Custom / Local (Ollama, CLIProxyAPI, etc)"
    read -p "  Choose [1/2/3/4]: " MODEL_CHOICE

    if [ "$MODEL_CHOICE" = "1" ]; then
        sed -i "s/MODEL_PROVIDER=gemini/MODEL_PROVIDER=gemini/" .env
        echo ""
        echo -e "${YELLOW}Gemini API Key${RESET}"
        echo "  Get it free at: https://aistudio.google.com/apikey"
        read -p "  Key: " GEMINI_KEY
        sed -i "s/your_gemini_api_key_here/$GEMINI_KEY/" .env

    elif [ "$MODEL_CHOICE" = "2" ]; then
        sed -i "s/MODEL_PROVIDER=gemini/MODEL_PROVIDER=openai/" .env
        sed -i "s/MODEL_NAME=gemini-2.0-flash/MODEL_NAME=gpt-4o/" .env
        read -p "  OpenAI API Key: " OPENAI_KEY
        sed -i "s/OPENAI_API_KEY=/OPENAI_API_KEY=$OPENAI_KEY/" .env

    elif [ "$MODEL_CHOICE" = "3" ]; then
        sed -i "s/MODEL_PROVIDER=gemini/MODEL_PROVIDER=openrouter/" .env
        sed -i "s/MODEL_NAME=gemini-2.0-flash/MODEL_NAME=google\/gemini-pro/" .env
        echo ""
        echo "  Get key at: https://openrouter.ai"
        read -p "  OpenRouter API Key: " OR_KEY
        sed -i "s/OPENROUTER_API_KEY=/OPENROUTER_API_KEY=$OR_KEY/" .env

    elif [ "$MODEL_CHOICE" = "4" ]; then
        sed -i "s/MODEL_PROVIDER=gemini/MODEL_PROVIDER=custom/" .env
        read -p "  Base URL (e.g. http://localhost:8317): " BASE_URL
        read -p "  API Key (or 'fake' for local): " CUSTOM_KEY
        read -p "  Model name: " MODEL_NAME
        sed -i "s|CUSTOM_BASE_URL=http://localhost:8317|CUSTOM_BASE_URL=$BASE_URL|" .env
        sed -i "s/CUSTOM_API_KEY=fake/CUSTOM_API_KEY=$CUSTOM_KEY/" .env
        sed -i "s/MODEL_NAME=gemini-2.0-flash/MODEL_NAME=$MODEL_NAME/" .env
    fi

    echo ""
    echo -e "${GREEN}✅ Configuration saved${RESET}"

    if [ "$PLATFORM_CHOICE" = "1" ]; then
        echo ""
        echo -e "${CYAN}${BOLD}Next Step:${RESET}"
        echo -e "  1. Your bot is ready for configuration."
        echo -e "  2. Once the app starts, go to Telegram and search for your bot."
        echo -e "  3. Send ${YELLOW}/start${RESET} to begin onboarding."
    fi
else
    echo -e "${GREEN}✅ .env exists — skipping setup${RESET}"
fi

# ── Launch ────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}${BOLD}  FriendlyClaw is starting...${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 main.py
