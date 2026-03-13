# FriendlyClaw 🦅 — Autonomous AI Operator

<p align="center">
  <strong>High-agency AI collaborator with system-level execution. Powered by OpenClaw.</strong>
</p>

---

FriendlyClaw is an **Autonomous AI Framework** designed for strategic collaboration and system management. It integrates persistent SQLite memory and diagnostic analysis with the comprehensive execution capabilities of **OpenClaw**.

### 🛡️ Data Sovereignty. 🧠 Eternal Memory. 🦾 System-Level Agency.

- **Persistent Partnership (Cognitive Persistence):** Unlike standard assistants, FriendlyClaw uses a local SQLite brain to remember every fact, preference, and historical context about you. It doesn't just chat; it evolves into a specialized digital operative that understands your unique workflow and objectives.
- **Unified System Body:** Ships with a built-in OpenClaw gateway, allowing your partner to physically operate your machine—executing shell commands, managing UI, and processing media.
- **Total Privacy:** 100% self-hosted. Your memories and system access tokens never leave your infrastructure.
- **High-Agency Execution:** Designed for users who need an AI that doesn't just suggest, but *acts* on their behalf with deep contextual awareness.

---

## ⚡ Deployment

### Option 1: Docker (Recommended)
Containerized environment for Core (Python) and Gateway (Node.js).
```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
cp .env.example .env
# Configure .env with API keys
docker compose up -d
```

### Option 2: Local Environment
Requires Node.js 22+ and Python 3.10+.
```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

---

## 🛠️ Operational Architecture

| Layer | Capabilities |
| :--- | :--- |
| **Logic (FriendlyClaw)** | `/analyze`, `/audit`, `/consult`, `/memory`. |
| **Execution (OpenClaw)** | `run_shell`, `type`, `click`, `screenshot`, and 50+ system skills. |
| **Extensibility** | Load any OpenClaw-compatible skill into `system_body/skills/`. |

---

## 🔌 Inference Models

FriendlyClaw is model-agnostic and interfaces via OpenAI-compatible APIs:
- **Cloud:** Gemini, GPT-4o, Claude 3.5.
- **Aggregators:** OpenRouter.
- **Local:** Ollama, LM Studio, or custom VLLM endpoints.

---

## 📂 System Structure

```
friendlyclaw/
├── main.py              # Unified entry point (Initializes Core + Gateway)
├── core/                # Agent logic & operational persona engine
├── memory/              # SQLite persistent context store
├── system_body/         # OpenClaw execution engine (Built-in)
├── platforms/           # Telegram & CLI communication layers
└── skills/              # Diagnostic & strategic modules
```

---

## 🚀 Vision
Built for the **Claw Ecosystem**. A strategic tool for elite technical operators.

---

## 📜 License
MIT.
