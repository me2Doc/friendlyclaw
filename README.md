# FriendlyClaw 🦅

<p align="center">
  <img src="assets/mascot.png" width="300" alt="FriendlyClaw Mascot">
</p>

<p align="center">
  <strong>Your self-hosted, persistent AI companion. Not an assistant. A partner.</strong>
</p>

---

FriendlyClaw is more than a chatbot—it’s an **Elite Personal Brain** that lives on your infrastructure. It doesn’t just answer questions; it remembers your history, understands your personality, and provides strategic analysis of your life, conversations, and decisions.

### 🛡️ Fully Owned. 🧠 Long-Term Memory. 🧬 Model Agnostic.

Most AIs are products you rent. **FriendlyClaw is a platform you own.** 

- **Total Sovereignty:** Runs on your server, your laptop, or the cloud. No corporate monitoring.
- **Eternal Memory:** Uses a local SQLite brain to remember every fact, event, and context you share.
- **Adaptive Personality:** You define who it is—from a direct strategic advisor to a casual companion.
- **Multimodal:** Send text, code, or screenshots. It sees what you see.

---

## ⚡ Quick Start

Deploy your companion in under 60 seconds.

```bash
git clone https://github.com/me2Doc/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

The `friendlyclaw.sh` script is an automated elite installer that handles environment setup, dependencies, and initial personality configuration.

---

## 🛠️ Core Capabilities

| Skill | Description |
| :--- | :--- |
| **`/analyze`** | Deconstruct complex social situations, screenshots, or chat logs. |
| **`/redflag`** | Scan interactions for manipulation, toxicity, or hidden patterns. |
| **`/opener`** | Generate high-impact, personalized openers based on your style. |
| **`/memory`** | Access what FriendlyClaw has learned about you across all sessions. |
| **`/advice`** | Get direct, unfiltered strategic advice based on your history. |

### 🧩 Add Custom Skills
FriendlyClaw is designed for modularity. You can add new skills without touching the core code. Simply drop a `.json` file into `skills/custom/`.

Example `skills/custom/joke.json`:
```json
{
    "trigger": "/joke",
    "description": "Tell a funny joke",
    "prompt": "Tell a joke that is actually funny and matches the user's style."
}
```
The bot will automatically detect the new command and add it to `/help`.

---

## 🔌 Bring Your Own Brain

FriendlyClaw is model-agnostic. Use the best models on the market or run locally for 100% privacy.

- **Cloud:** Gemini 2.0/3.0, GPT-4o, Claude 3.5.
- **Aggregators:** OpenRouter (access 100+ models).
- **Local:** Ollama, LM Studio, or any OpenAI-compatible API.

---

## 🚀 Deploy 24/7 (Railway / VPS)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repo.
2. Connect to Railway.
3. Add your `TELEGRAM_BOT_TOKEN` and `GEMINI_API_KEY`.
4. Set `PLATFORM=telegram`.

---

## 📂 Architecture

FriendlyClaw is built for modularity and speed:

```
friendlyclaw/
├── main.py              # Single entry point
├── core/                # Agent logic & personality engines
├── memory/              # SQLite persistent long-term memory
├── platforms/           # Telegram & CLI interfaces
├── skills/              # Specialized analysis modules
└── assets/              # Branding & media
```

---

## 🗺️ Roadmap

- [ ] **WhatsApp & Discord Integration**
- [ ] **Voice-to-Voice (Whisper/TTS) support**
- [ ] **Real-time Web Dashboard**
- [ ] **Vision-based profile analysis**

---

## 📜 License

MIT. Take it, fork it, make it yours.

*Built for the Claw Ecosystem.*
