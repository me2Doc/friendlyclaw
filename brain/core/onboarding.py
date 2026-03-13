import os
from brain.memory.memory import save_profile, get_profile, init_db

QUESTIONS = [
    {
        "key": "user_name",
        "text": "Identify primary user:",
        "required": True
    },
    {
        "key": "agent_name",
        "text": "Set Agent Designation (System Identity):",
        "required": True
    },
    {
        "key": "agent_personality",
        "text": "Define Operational Persona (Engagement Strategy):\n\nExamples: *Direct and Objective*, *Technical Specialist*, *Strategic Analyst*\n\nSet your desired interaction mode.",
        "required": True
    },
    {
        "key": "agent_tone",
        "text": "Select Communication Protocol (Formal / Casual / Concise):",
        "required": True
    },
    {
        "key": "user_context",
        "text": "Provide high-level user context (Objectives, technical environment, persistent data):\n\nOr input *skip*.",
        "required": False
    }
]


def get_onboarding_state(user_id: str) -> dict:
    """Returns current initialization state for user"""
    profile = get_profile(user_id)
    if profile.get("onboarded"):
        return {"done": True}
    step = profile.get("onboarding_step", 0)
    return {"done": False, "step": step, "profile": profile}


def get_current_question(step: int) -> dict:
    if step < len(QUESTIONS):
        return QUESTIONS[step]
    return None


def process_onboarding_answer(user_id: str, answer: str, image_bytes: bytes = None) -> dict:
    """Process an initialization parameter, return next step or completion"""
    profile = get_profile(user_id)
    step = profile.get("onboarding_step", 0)

    if step >= len(QUESTIONS):
        profile["onboarded"] = True
        save_profile(user_id, profile)
        return {"done": True}

    question = QUESTIONS[step]
    key = question["key"]

    if answer.strip().lower() == "skip" and not question["required"]:
        profile[key] = ""
    else:
        profile[key] = answer.strip()

    profile["onboarding_step"] = step + 1
    save_profile(user_id, profile)

    next_step = step + 1
    if next_step >= len(QUESTIONS):
        profile["onboarded"] = True
        profile["onboarding_step"] = next_step
        save_profile(user_id, profile)
        return {
            "done": True,
            "agent_name": profile.get("agent_name", "Agent"),
            "user_name": profile.get("user_name", "User")
        }

    return {
        "done": False,
        "next_question": QUESTIONS[next_step]["text"],
        "step": next_step,
        "total": len(QUESTIONS)
    }


def get_welcome_message() -> str:
    return (
        "**FriendlyClaw System Initialization**\n\n"
        "Autonomous AI Operator Framework (Powered by OpenClaw)\n"
        "Persistent context enabled. Strategic alignment active.\n\n"
        f"{QUESTIONS[0]['text']}"
    )
