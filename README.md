# FriendlyClaw 🦅 — Autonomous AI Operator

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.2.0--Alpha-orange.svg" alt="Version">
  <img src="https://img.shields.io/badge/Body-OpenClaw-green.svg" alt="Powered by OpenClaw">
  <img src="https://img.shields.io/badge/Architecture-Brain_%2B_Body-blueviolet.svg" alt="Architecture">
</p>

<p align="center">
  <strong>High-agency AI collaborator with system-level execution. Powered by OpenClaw.</strong>
</p>

---

## 🦾 Unified Intelligence & Action

FriendlyClaw is an **Autonomous AI Framework** that bridges the gap between conversational intelligence and physical system execution. It is built on a "Brain & Body" architecture:

- **The Brain (FriendlyClaw Core):** A Python-based intelligence layer with **Cognitive Persistence** (SQLite-backed long-term memory) and strategic analysis modules.
- **The Body (OpenClaw Engine):** A Node.js-based execution gateway that provides direct access to your machine's shell, UI, media, and 50+ specialized system skills.

---

## 🧠 Key Features

### 🛡️ Data Sovereignty & Privacy
100% self-hosted. Your persistent memories, interaction history, and system access tokens never leave your infrastructure. You choose the inference model (Local or Cloud).

### 🧠 Cognitive Persistence (Eternal Memory)
Unlike standard chatbots that forget once the session ends, FriendlyClaw uses a local SQLite brain to store every fact, preference, and historical context about you. It evolves into a **high-fidelity digital operative** that understands your specific workflows.

### 🦾 High-Agency Execution
FriendlyClaw doesn't just suggest actions—it executes them. Interfaced via the OpenClaw protocol, it can operate your shell, move your mouse, type on your behalf, and process system-level data in real-time.

---

## ⚡ Quick Start

The fastest way to get FriendlyClaw up and running:

```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

The script will walk you through setting up your API keys and choosing between **CLI** or **Telegram** mode.

---

## 🤖 Telegram Bot Setup (If choosing Telegram)

Setting up your bot only takes a minute:

1.  **Open Telegram** and search for **@BotFather**.
2.  Send `/newbot` and follow the prompts (give it a name and a username).
3.  **Copy the API Token** provided by @BotFather.
4.  Paste this token when the `friendlyclaw.sh` script asks for it.
5.  Once the app is running, find your bot in Telegram and send **`/start`** to begin!

---

## 🏗️ Requirements

- **Python 3.10+**
- **Node.js 22.12.0+** (Required for the OpenClaw "Body")
- An API Key (Gemini is recommended and free!)

---

## 🛠️ Operational Architecture

FriendlyClaw presents a unified command set while delegating tasks between layers:

| Module | Purpose | Example Triggers |
| :--- | :--- | :--- |
| **Logic Layer** | Cognitive/Strategic Tasks | `/analyze`, `/audit`, `/consult`, `/memory` |
| **Action Layer** | System Execution | `run_shell`, `type`, `click`, `screenshot` |
| **System Skills** | Domain-Specific Tools | `xurl`, `spotify`, `gh-issues`, `weather` |

---

## 🎯 Strategic Workflows

- **Context-Aware Coding:** Ask your partner to "Update the auth logic in my project" using the built-in `run_shell` and `gh-issues` skills.
- **System Automation:** "Open Chromium and search for the latest documentation on VLLM."
- **Persistent Memory:** FriendlyClaw remembers that you prefer certain coding styles or deployment environments and applies that context to future tasks without being reminded.
- **Security Auditing:** Use `/audit` to analyze logs or external data for hidden patterns or misalignments.

---

## 🧩 Extensibility

FriendlyClaw supports a dual-skill architecture, allowing you to extend both its intelligence and its physical capabilities.

### 1. Native System Skills (OpenClaw Body)
To add new physical capabilities (e.g., controlling a new app or API), drop an OpenClaw-compatible skill folder into `system_body/skills/`.
- FriendlyClaw will automatically detect these on boot.
- The AI will understand how to use these new "muscles" natively.

### 2. Logic Extensions (FriendlyClaw Brain)
To add new analytical commands or persona-specific logic, drop a `.json` file into `skills/custom/`.
Example `skills/custom/custom_audit.json`:
```json
{
    "trigger": "/custom_audit",
    "description": "Perform a specialized security audit",
    "prompt": "Analyze the following for specific alignment with [Your Custom Policy]..."
}
```

---

## 🔌 Inference Models

Model-agnostic and interfaces via OpenAI-compatible APIs:
- **Cloud:** Gemini, GPT-4o, Claude 3.5.
- **Aggregators:** OpenRouter (access 100+ models).
- **Local:** Ollama, LM Studio, or custom VLLM endpoints.

---

## 📂 System Structure

```
friendlyclaw/
├── main.py              # Unified entry point (Initializes Core + Gateway)
├── core/                # Agent logic & operational persona engine
├── memory/              # SQLite persistent context store (The Brain)
├── system_body/         # OpenClaw execution engine (The Body)
├── platforms/           # Telegram & CLI communication layers
└── skills/              # Strategic & diagnostic modules
```

---

## 🚀 Vision
Built for the **Claw Ecosystem**. A strategic tool for elite technical operators who need a partner that acts as a digital extension of their own agency.

---

## 📜 License
MIT.
