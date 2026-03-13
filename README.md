# FriendlyClaw 🦅 — Autonomous AI Operator

<p align="center">
  <strong>High-agency AI collaborator with system-level execution. Powered by OpenClaw.</strong>
</p>

---

FriendlyClaw is an **Autonomous AI Framework** designed for strategic collaboration and system management. It integrates persistent SQLite memory and diagnostic analysis with the comprehensive execution capabilities of **OpenClaw**.

### 🛡️ Data Sovereignty. 🧠 Persistent Context. 🦾 System Execution.

- **Private Deployment:** Fully self-hosted on personal infrastructure. You own the model and the data.
- **Persistent Logic:** Uses a local SQLite store to maintain context and directives across sessions.
- **Unified Gateway:** Includes a built-in OpenClaw gateway for system control (Shell, UI, Media, 50+ Skills).
- **High Agency:** Designed to execute complex system tasks and provide objective strategic analysis.

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
