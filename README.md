experimental phase 
# FriendlyClaw 🦀 — Autonomous Hive Operative

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Edition-Hive-orange.svg" alt="Hive Edition">
  <img src="https://img.shields.io/badge/Memory-Eternal--RAG-green.svg" alt="Memory">
  <img src="https://img.shields.io/badge/Platform-Telegram--CLI-blueviolet.svg" alt="Platforms">
</p>

<p align="center">
  <img src="assets/mascot.png" width="300" alt="FriendlyClaw Mascot">
</p>

<p align="center">
  <strong>Recursive Brain</strong> • <strong>Multi-Agent Swarm</strong> • <strong>Self-Healing Body</strong> • <strong>Eternal Memory</strong>
</p>

<p align="center">
  <strong>The Professional AI Strategic Partner for Elite Operators.</strong><br>
  A unified "Brain & Body" architecture for total system control via CLI or Telegram.
</p>

---

## 🚀 Why FriendlyClaw?

FriendlyClaw is not a "chatbot." It is a **Sovereign Digital Operative**. While standard AI assistants wait for you to type and forget what you said yesterday, FriendlyClaw Hive lives on your system, works while you sleep, and retrieves your entire history semantically.

### 📊 Comparison: Partner vs. Assistant

| Feature | Standard Assistants | **FriendlyClaw Hive** |
| :--- | :--- | :--- |
| **Agency** | Reactive (Waits for input) | **Proactive (Heartbeat + Missions)** |
| **Memory** | Linear (Forgets over time) | **Eternal (SQLite-Vec RAG)** |
| **Execution** | Text-only / Sandbox | **System-Wide (50+ Native Skills)** |
| **Concurrency** | Single-threaded | **Multi-threaded (Swarm Workers)** |
| **Reliability** | Crashes = Manual Restart | **Self-Healing (Watchdog Loop)** |
| **Privacy** | SaaS-owned logs | **100% Local SQLite Brain** |

---

## 💎 Core Hive Capabilities

### 🐝 1. Swarm Commander (Parallel Intelligence)
The Commander Brain (`brain/core/agent.py`) can spawn **Ghost Workers** to handle heavy lifting in the background.
- **Delegate & Continue:** Ask your partner to "Research RISC-V history" while you continue talking about your current code.
- **Task Board:** Track every background mission via `/tasks` and pull results with `/synthesize`.

### 🧠 2. Eternal Memory (Semantic RAG)
Powered by `sqlite-vec`, FriendlyClaw performs a **768-dim vector search** on every turn.
- **Deep Retrieval:** It remembers preferences, technical decisions, and context from months ago.
- **Fact Extraction:** Automatically commits important system data to its long-term factual store.

### 🛡️ 3. Vault-Grade Security (Human-in-the-Loop)
We believe in **High Agency with High Accountability**.
- **Permission Intercept:** Every shell command triggers a UI prompt. It only runs once you click **Confirm**.
- **Workspace Sandbox:** Set a `WORKSPACE_ROOT` to lock the AI inside a specific directory, preventing accidental system-wide escapes.

### 💓 4. Proactive Heartbeat (The Sentinel)
FriendlyClaw checks your `HEARTBEAT.md` file every 15 minutes.
- **Autonomous Missions:** "Monitor my server temperature," "Check for GitHub PRs," or "Audit logs for anomalies."
- **Visual Pulse:** The agent can use camera snapshots or screen captures to "look" at its environment and report findings.

---

## 🔗 Unified Model Fallback

FriendlyClaw is indestructible. If your primary API fails, it automatically rolls over to ensure your missions never stop.

1.  **Gemini 2.0 Flash** (Fastest, Multi-modal, Default)
2.  **OpenRouter** (Access to Claude 3.5, Llama 3, etc.)
3.  **OpenAI GPT-4o** (Reliable Logic)
4.  **Local Ollama** (100% Private Fallback)

---

## ⚡ Quick Start (2-Minute Setup)

```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

> [!TIP]
> The setup script is an **interactive wizard**. It will check your dependencies (Node 22+, Python 3.10+), create your virtual environment, and walk you through API key configuration.

---

## 🕹️ Essential Commands

| Command | Action |
| :--- | :--- |
| `/tasks` | View the background mission board. |
| `/synthesize [id]` | Merge sub-agent findings into the chat. |
| `/memory` | Query the AI's factual knowledge of you. |
| `/model [name]` | Hot-swap models (e.g., `/model gpt-4o`). |
| `/forget` | Wipe all local cognitive history. |

---

## 🧠 Architecture: Brain & Body

The Hive is organized for technical excellence and modularity:

- **`brain/`**: The Intelligence Layer (Python). Reasoning, Swarm management, and Semantic Memory.
- **`body/`**: The Execution Layer (Node.js). Powered by OpenClaw with 50+ hooks (Shell, Spotify, Media, GitHub).
- **`tools/`**: Professional research integrations like **Scrapling-Netrunner** for deep web intelligence.
- **`data/`**: Your sovereign data vault. Logs, vectors, and the SQLite Hive database.

---

## 🚀 Vision
FriendlyClaw is the digital extension of human agency. It is built for elite technical operators who need a partner that acts as a secure, proactive, and multi-threaded interface to their machine and the web.

---

## 📚 Deep Documentation
- **[🧠 Architecture Deep-Dive](./docs/architecture/HIVE_MIND.md)**
- **[🕹️ Full Command Reference](./docs/guides/COMMANDS.md)**
- **[🛠️ Professional Setup Guide](./docs/guides/SETUP.md)**

---

## 📜 License
MIT. Built for the **Claw Ecosystem**.
