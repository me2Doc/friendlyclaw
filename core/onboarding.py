import os
from memory.memory import save_profile, get_profile, init_db

QUESTIONS = [
    {
        "key": "user_name",
        "text": "What should I call you?",
        "required": True
    },
    {
        "key": "agent_name",
        "text": "What do you want to name me? (your call — could be anything)",
        "required": True
    },
    {
        "key": "agent_personality",
        "text": "How should I come across? Describe the vibe.\n\nExamples: *chill and loyal*, *brutally honest*, *funny and sharp*, *calm and supportive*\n\nJust write whatever feels right.",
        "required": True
    },
    {
        "key": "agent_tone",
        "text": "Formal or casual? Or somewhere in between?",
        "required": True
    },
    {
        "key": "user_context",
        "text": "Tell me about yourself — whatever you want me to know. Interests, job, personality, what's going on in your life.\n\nOr say *skip*.",
        "required": False
    },
    {
        "key": "visual_context",
        "text": "Optional: describe or send a photo of who you imagine me as — an anime character, a person, a vibe. Helps me understand the aesthetic in your head.\n\nSay *skip* to skip this.",
        "required": False,
        "accepts_photo": True
    }
]


def get_onboarding_state(user_id: str) -> dict:
    """Returns current onboarding state for user"""
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
    """Process an onboarding answer, return next question or completion"""
    profile = get_profile(user_id)
    step = profile.get("onboarding_step", 0)

    if step >= len(QUESTIONS):
        profile["onboarded"] = True
        save_profile(user_id, profile)
        return {"done": True}

    question = QUESTIONS[step]
    key = question["key"]

    # Handle skip
    if answer.strip().lower() == "skip" and not question["required"]:
        profile[key] = ""
    elif image_bytes and question.get("accepts_photo"):
        profile[key] = f"[User sent a reference image for visual context]"
        profile["has_visual_ref"] = True
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
            "agent_name": profile.get("agent_name", "Buddy"),
            "user_name": profile.get("user_name", "friend")
        }

    return {
        "done": False,
        "next_question": QUESTIONS[next_step]["text"],
        "step": next_step,
        "total": len(QUESTIONS)
    }


def get_welcome_message() -> str:
    return (
        "👋 Hey. I'm *FriendlyClaw* — your personal AI.\n\n"
        "Not a chatbot. Not an assistant. A companion.\n"
        "I'll remember everything you tell me. I'll give you real talk.\n"
        "You define who I am.\n\n"
        "Let's set this up. Takes 2 minutes.\n\n"
        f"{QUESTIONS[0]['text']}"
    )
