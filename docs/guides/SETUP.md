# 🛠️ FriendlyClaw Setup Guide

This guide covers the professional deployment of FriendlyClaw Hive, from local development to production-ready configurations.

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 22.12.0+**
- **Git**
- An API Key from one of the following:
  - [Google AI Studio](https://aistudio.google.com/) (Gemini - Recommended & Free tier available)
  - [OpenRouter](https://openrouter.ai/) (Access to 100+ models)
  - [OpenAI](https://platform.openai.com/)

---

## 🚀 Installation

### 1. Clone the Hive
```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
```

### 2. Run the Interactive Wizard
The easiest way to get started is the `friendlyclaw.sh` script. It handles virtual environment creation, dependency installation, and `.env` configuration.
```bash
chmod +x friendlyclaw.sh
./friendlyclaw.sh
```

---

## 🤖 Telegram Bot Configuration

1. **Find @BotFather** on Telegram.
2. Send `/newbot` and follow the instructions.
3. **Copy the API Token**.
4. In the `friendlyclaw.sh` wizard, choose the **Telegram** platform and paste your token when prompted.
5. Search for your bot on Telegram and send **`/start`**.

---

## 🛡️ Hardening & Security

### Workspace Sandboxing
By default, FriendlyClaw has a "Sandbox Lite" feature. To restrict the AI's ability to edit files outside of your project directory, set the following in your `.env`:

```env
WORKSPACE_ROOT=/home/user/my_project_folder
```

Commands that attempt to modify files outside this path will be blocked by the security bridge.

---

## 🧠 Using Local Models (Ollama)

FriendlyClaw supports local LLMs for 100% private operations.
1. Install [Ollama](https://ollama.com/).
2. Run your preferred model (e.g., `ollama run llama3`).
3. Ensure the Ollama API is accessible (usually at `http://localhost:11434`).
4. Update your `.env`:
```env
CUSTOM_BASE_URL=http://localhost:11434/v1
CUSTOM_API_KEY=ollama
```

---

## ❓ Troubleshooting

### Circular Import Errors
Ensure you are using the latest version of the Hive (v3+). We moved prompts to `core/prompts.py` to solve this.

### Database Locked
If you see `sqlite3.OperationalError: database is locked`, it means multiple swarm workers are writing simultaneously. We have a 20s timeout built-in, but ensure your disk I/O isn't heavily saturated.

### Bot Not Responding
Check the logs in `data/friendlyclaw.log`. Ensure your `OPENCLAW_WS_URL` is correct (default is `ws://127.0.0.1:18789`).
