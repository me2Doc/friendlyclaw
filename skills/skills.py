import os
import json
import logging
from pathlib import Path

logger = logging.getLogger("FriendlyClaw.Skills")

# Core skills that are always included
CORE_SKILLS = {
    "analyze": {
        "trigger": "/analyze",
        "description": "Analyze any conversation, situation, or text",
        "prompt": "The user wants you to analyze something. Break it down: what's actually happening, what the other person's intentions seem to be, what the user should know, and what they should do. Be direct. No fluff."
    },
    "redflag": {
        "trigger": "/redflag",
        "description": "Check for red flags in a situation or conversation",
        "prompt": "Scan what the user shares for red flags. Be specific — list exactly what concerned you and why. Also note green flags if there are any. Give a verdict at the end."
    },
    "reply": {
        "trigger": "/reply",
        "description": "Help write a reply to a message",
        "prompt": "The user needs help writing a reply. Give them 2-3 options with different tones. Match their personality and communication style. Label each option clearly (e.g. Direct / Playful / Neutral)."
    },
    "opener": {
        "trigger": "/opener",
        "description": "Generate a conversation opener",
        "prompt": "Write an opener for the user based on what they describe. Make it personal and specific — not generic. Give 3 options with different energies. If they haven't given enough info, ask first."
    },
    "vent": {
        "trigger": "/vent",
        "description": "Just listen and respond like a friend",
        "prompt": "The user needs to vent. Listen. Respond like a real friend would — acknowledge what they're feeling, give your honest take if they seem to want it, but don't turn this into a therapy session. Keep it real."
    },
    "advice": {
        "trigger": "/advice",
        "description": "Get direct advice on any situation",
        "prompt": "Give direct, actionable advice. Don't hedge. Don't add disclaimers. Tell them what you'd actually do in their position and why."
    },
    # System commands handled by platform logic
    "memory": {"trigger": "/memory", "description": "See what I remember about you", "system": True},
    "forget": {"trigger": "/forget", "description": "Wipe memory and start fresh", "system": True},
    "model": {"trigger": "/model", "description": "Switch AI model", "system": True},
    "help": {"trigger": "/help", "description": "Show all commands", "system": True}
}

CUSTOM_SKILLS_DIR = Path("skills/custom")

def load_custom_skills() -> dict:
    """Loads all .json skill files from the custom skills directory"""
    skills = {}
    if not CUSTOM_SKILLS_DIR.exists():
        CUSTOM_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        return skills

    for skill_file in CUSTOM_SKILLS_DIR.glob("*.json"):
        try:
            with open(skill_file, "r") as f:
                skill_data = json.load(f)
                # Basic validation: must have trigger and description
                if "trigger" in skill_data and "prompt" in skill_data:
                    skill_name = skill_file.stem
                    skills[skill_name] = skill_data
                    logger.info(f"Loaded custom skill: {skill_name} ({skill_data['trigger']})")
        except Exception as e:
            logger.error(f"Failed to load custom skill {skill_file}: {e}")
    
    return skills

def get_all_skills() -> dict:
    """Combines core and custom skills into one dictionary"""
    all_skills = CORE_SKILLS.copy()
    all_skills.update(load_custom_skills())
    return all_skills

def get_skill_prompt(trigger: str) -> str:
    """Returns the skill prompt injection for a given trigger"""
    all_skills = get_all_skills()
    for skill_name, skill in all_skills.items():
        if skill.get("trigger") == trigger and not skill.get("system"):
            return skill["prompt"]
    return None

def get_help_text() -> str:
    """Generates help text based on all currently loaded skills"""
    all_skills = get_all_skills()
    lines = ["*Available commands:*\n"]
    
    # Sort triggers alphabetically
    sorted_skills = sorted(all_skills.items(), key=lambda x: x[1]['trigger'])
    
    for skill_name, skill in sorted_skills:
        lines.append(f"`{skill['trigger']}` — {skill.get('description', 'No description')}")
    
    lines.append("\nOr just talk to me normally.")
    return "\n".join(lines)
