# FriendlyClaw Custom Skills 🧩

FriendlyClaw is designed to be infinitely extensible. You can add new "brains" or "capabilities" by simply dropping a `.json` file into this directory (`skills/custom/`).

## How to Add a Skill

1.  Create a new `.json` file in this folder (e.g., `my_skill.json`).
2.  Define the `trigger`, `description`, and `prompt`.
3.  Restart FriendlyClaw (or wait for the next interaction).

## JSON Schema

Each skill file must follow this format:

```json
{
    "trigger": "/command",
    "description": "What this skill does (shown in /help)",
    "prompt": "The system prompt instruction injected when this skill is active."
}
```

### Example: `weather.json`
```json
{
    "trigger": "/weather",
    "description": "Analyze weather conditions for a location",
    "prompt": "The user wants a weather analysis. Don't just give numbers; tell them how it feels, what to wear, and if they should stay inside. Be direct and personal."
}
```

## Community Skills
You can pull skills from the **OpenClaw** community repo and drop them here. FriendlyClaw will automatically pick them up and route them to your chosen AI model (Gemini, GPT-4, etc.).

---
*Built for the Claw Ecosystem.*
