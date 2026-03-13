"""
Pre-installed skills for FriendlyClaw.
Each skill is triggered by a command or keyword.
"""

SKILLS = {
    "analyze": {
        "trigger": "/analyze",
        "description": "Analyze any conversation, situation, or text",
        "prompt": """The user wants you to analyze something. 
        Break it down: what's actually happening, what the other person's intentions seem to be, 
        what the user should know, and what they should do. Be direct. No fluff."""
    },
    "redflag": {
        "trigger": "/redflag",
        "description": "Check for red flags in a situation or conversation",
        "prompt": """Scan what the user shares for red flags. 
        Be specific — list exactly what concerned you and why. 
        Also note green flags if there are any. Give a verdict at the end."""
    },
    "reply": {
        "trigger": "/reply",
        "description": "Help write a reply to a message",
        "prompt": """The user needs help writing a reply. 
        Give them 2-3 options with different tones. 
        Match their personality and communication style. 
        Label each option clearly (e.g. Direct / Playful / Neutral)."""
    },
    "opener": {
        "trigger": "/opener",
        "description": "Generate a conversation opener",
        "prompt": """Write an opener for the user based on what they describe. 
        Make it personal and specific — not generic. 
        Give 3 options with different energies. 
        If they haven't given enough info, ask first."""
    },
    "vent": {
        "trigger": "/vent",
        "description": "Just listen and respond like a friend",
        "prompt": """The user needs to vent. 
        Listen. Respond like a real friend would — acknowledge what they're feeling, 
        give your honest take if they seem to want it, 
        but don't turn this into a therapy session. Keep it real."""
    },
    "advice": {
        "trigger": "/advice",
        "description": "Get direct advice on any situation",
        "prompt": """Give direct, actionable advice. 
        Don't hedge. Don't add disclaimers. 
        Tell them what you'd actually do in their position and why."""
    },
    "memory": {
        "trigger": "/memory",
        "description": "See what I remember about you",
        "system": True  # handled in bot, not as a prompt
    },
    "forget": {
        "trigger": "/forget",
        "description": "Wipe memory and start fresh",
        "system": True
    },
    "model": {
        "trigger": "/model",
        "description": "Switch AI model",
        "system": True
    },
    "help": {
        "trigger": "/help",
        "description": "Show all commands",
        "system": True
    }
}


def get_skill_prompt(trigger: str) -> str:
    """Returns the skill prompt injection for a given trigger"""
    for skill_name, skill in SKILLS.items():
        if skill.get("trigger") == trigger and not skill.get("system"):
            return skill["prompt"]
    return None


def get_help_text() -> str:
    lines = ["*Available commands:*\n"]
    for skill_name, skill in SKILLS.items():
        lines.append(f"`{skill['trigger']}` — {skill['description']}")
    lines.append("\nOr just talk to me normally.")
    return "\n".join(lines)
