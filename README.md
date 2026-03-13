# FriendlyClaw 🦅 — Standalone AI Operator

<p align="center">
  <img src="assets/mascot.png" width="300" alt="FriendlyClaw Mascot">
</p>

<p align="center">
  <strong>The open-source AI companion with a system-level body. Powered by OpenClaw.</strong>
</p>

---

FriendlyClaw is an **Elite Personal Brain** that lives on your infrastructure. It combines long-term persistent memory and strategic analysis with the physical system-execution capabilities of the **OpenClaw** ecosystem.

### 🛡️ Fully Owned. 🧠 Long-Term Memory. 🦾 System-Level Execution.

- **Total Sovereignty:** Runs on your server, laptop, or cloud. You own the data.
- **Eternal Memory:** Uses a local SQLite brain to remember facts across all sessions.
- **Unified Body:** Ships with a built-in OpenClaw gateway to control your computer (Shell, UI, Media).
- **Multimodal:** Process text, code, or screenshots. It sees and acts.

---

## ⚡ Quick Start

Deploy your standalone operator in under 60 seconds.

### Option 1: Docker (Recommended)
The cleanest way to run the Brain (Python) and Body (Node.js) together.
```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
```

### Option 2: Local Script
Requires Node.js 22+ and Python 3.10+.
```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

---

## 🛠️ Integrated Capabilities

| Layer | Features |
| :--- | :--- |
| **Brain (FriendlyClaw)** | `/analyze`, `/audit`, `/memory`, `/advice`, `/reply`, `/opener`. |
| **Body (OpenClaw)** | `run_shell`, `type`, `click`, `screenshot`, and 50+ system skills. |
| **Modular Skills** | Add any OpenClaw-compatible skill to `system_body/skills/`. |

### 🧩 System Control
FriendlyClaw is physically connected to your system. When you ask it to perform an action (e.g., *"Open Chromium"* or *"Search for files"*), it uses its internal OpenClaw body to execute the command directly on your machine.

---

## 🔌 Model Agnostic

Use any model as the "Brain":
- **Cloud:** Gemini 2.0/3.0, GPT-4o, Claude 3.5.
- **Aggregators:** OpenRouter.
- **Local:** Ollama, LM Studio, or any OpenAI-compatible API.

---

## 📂 Standalone Architecture

FriendlyClaw is a unified system:

```
friendlyclaw/
├── main.py              # Unified entry point (Starts Brain + Body)
├── core/                # Agent logic & personality engine
├── memory/              # SQLite persistent long-term memory
├── system_body/         # Built-in OpenClaw execution engine (Gateway + 50+ Skills)
├── platforms/           # Telegram & CLI interfaces
└── skills/              # Specialized analysis modules
```

---

## 🚀 Public & Extensible
Built for the **Claw Ecosystem**. Take it, fork it, and build your own operator.

---

## 📜 License
MIT.
