import os
import json
import logging
from pathlib import Path

logger = logging.getLogger("FriendlyClaw.Skills")

# Core operational modules
CORE_SKILLS = {
    "analyze": {
        "trigger": "/analyze",
        "description": "Comprehensive analysis of technical data, logs, or strategic contexts",
        "prompt": "Perform a deep-dive analysis. Identify core patterns, technical implications, and strategic outcomes. Provide a structured report with actionable insights."
    },
    "audit": {
        "trigger": "/audit",
        "description": "Security and intent audit for external inputs or system states",
        "prompt": "Execute an audit. Identify potential risks, hidden vectors, or misalignments. Provide a high-confidence assessment of the input's integrity."
    },
    "consult": {
        "trigger": "/consult",
        "description": "Strategic consultation on complex decision-making or system architecture",
        "prompt": "Provide high-agency strategic advice. Base your recommendations on the available context and long-term objectives. Avoid generic disclaimers; provide a clear path forward."
    },
    # System commands handled by platform logic
    "memory": {"trigger": "/memory", "description": "Query the persistent memory store", "system": True},
    "forget": {"trigger": "/forget", "description": "Reset local memory and operational profile", "system": True},
    "model": {"trigger": "/model", "description": "Hot-swap the active inference model", "system": True},
    "help": {"trigger": "/help", "description": "Display system documentation and capabilities", "system": True}
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
                if "trigger" in skill_data and "prompt" in skill_data:
                    skill_name = skill_file.stem
                    skills[skill_name] = skill_data
                    logger.info(f"Loaded extension: {skill_name} ({skill_data['trigger']})")
        except Exception as e:
            logger.error(f"Failed to load extension {skill_file}: {e}")
    
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

def get_openclaw_skills() -> list:
    """Reads the system_body/skills directory to find available OpenClaw system skills"""
    skills_dir = Path("system_body/skills")
    if not skills_dir.exists() or not skills_dir.is_dir():
        return []
    
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)
    return sorted(skills)

def get_help_text() -> str:
    """Generates help text based on all currently loaded skills"""
    all_skills = get_all_skills()
    lines = ["*Operational Modules (Core):*\n"]
    
    sorted_skills = sorted(all_skills.items(), key=lambda x: x[1]['trigger'])
    
    for skill_name, skill in sorted_skills:
        lines.append(f"`{skill['trigger']}` — {skill.get('description', 'No description')}")
    
    oc_skills = get_openclaw_skills()
    if oc_skills:
        lines.append("\n*System Execution Skills (Native Body):*\n")
        lines.append(", ".join([f"`{s}`" for s in oc_skills]))

    lines.append("\nInput may be provided in natural language.")
    return "\n".join(lines)
