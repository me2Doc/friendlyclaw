# FriendlyClaw 🦅

**Your personal AI companion. Self-hosted. Remembers everything.**

FriendlyClaw is an open-source AI companion you fully own. Define its personality, connect it to Telegram or run it in your terminal, and it remembers every conversation. Bring your own model — Gemini, GPT, Claude, local LLM, anything.

Not a chatbot. Not a product. Yours.

---

## Install

```bash
git clone https://github.com/yourusername/friendlyclaw
cd friendlyclaw
chmod +x friendlyclaw.sh && ./friendlyclaw.sh
```

That's it. The script handles everything — dependencies, config, model selection, platform setup.

---

## What It Does

- **Remembers everything** — persistent SQLite memory across all sessions
- **You define the personality** — name it, give it a tone, a style, an attitude
- **Analyzes anything** — paste conversations, screenshots, situations
- **Model agnostic** — Gemini, OpenAI, OpenRouter, local LLM, custom endpoint
- **Multi-platform** — Telegram bot or CLI
- **Skill system** — built-in commands for common tasks

---

## Commands

| Command | What it does |
|---------|-------------|
| `/analyze` | Break down any conversation or situation |
| `/redflag` | Scan for red flags |
| `/reply` | Get reply suggestions |
| `/opener` | Generate a personalized opener |
| `/vent` | Just talk — it listens |
| `/advice` | Direct, no-BS advice |
| `/memory` | See what it remembers about you |
| `/forget` | Wipe memory and start fresh |
| `/model` | Check or switch model |
| `/help` | All commands |

Or just talk to it normally.

---

## Model Support

Change `MODEL_PROVIDER` and `MODEL_NAME` in your `.env`:

| Provider | Example models | Notes |
|----------|---------------|-------|
| `gemini` | `gemini-2.0-flash`, `gemini-2.5-pro` | Free tier available |
| `openai` | `gpt-4o`, `gpt-4o-mini` | Paid |
| `openrouter` | `google/gemini-pro`, `meta-llama/llama-3.1-8b` | 100+ models, some free |
| `custom` | anything | Ollama, CLIProxyAPI, LM Studio, any OpenAI-compatible endpoint |

Switch model mid-session: `/model gemini-2.5-pro`

---

## Deploy 24/7 (Free)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

Add these env vars on Railway:
- `TELEGRAM_BOT_TOKEN`
- `GEMINI_API_KEY` (or your chosen provider's key)
- `MODEL_PROVIDER=gemini`
- `MODEL_NAME=gemini-2.0-flash`
- `PLATFORM=telegram`

---

## Self-Host on Your Server

```bash
git clone https://github.com/yourusername/friendlyclaw
cd friendlyclaw
cp .env.example .env
# Edit .env with your keys
pip install -r requirements.txt
python3 main.py --telegram  # or --cli
```

---

## Project Structure

```
friendlyclaw/
├── main.py              # Entry point
├── friendlyclaw.sh      # One-command install
├── requirements.txt
├── .env.example
├── core/
│   ├── agent.py         # Core AI logic, model routing
│   └── onboarding.py    # Personality setup flow
├── memory/
│   └── memory.py        # SQLite persistent memory
├── skills/
│   └── skills.py        # Built-in skill system
├── platforms/
│   ├── telegram_bot.py  # Telegram interface
│   └── cli.py           # Terminal interface
└── data/                # Local DB (gitignored)
```

---

## Roadmap

- [ ] WhatsApp support
- [ ] Discord support  
- [ ] Voice message support
- [ ] Web UI
- [ ] Plugin system for custom skills
- [ ] Photo analysis of profiles/people
- [ ] Scheduled check-ins

---

## Contributing

PRs welcome. Keep it lean and real — no bloat, no corporate patterns.

---

## License

MIT — take it, fork it, build on it.

---

*Part of the Claw ecosystem.*
