import asyncio
import os
from core.agent import chat
from core.onboarding import (
    get_onboarding_state, process_onboarding_answer, get_welcome_message
)
from memory.memory import (
    init_db, get_profile, clear_user, 
    get_pending_action, delete_pending_action
)
from skills.skills import get_skill_prompt, get_help_text, get_all_skills

USER_ID = "cli_user"

async def cli_chat():
    init_db()
    print("\n" + "="*50)

    state = get_onboarding_state(USER_ID)

    if not state["done"]:
        print(get_welcome_message().replace("*", ""))
        print()

        while True:
            state = get_onboarding_state(USER_ID)
            if state["done"]:
                break

            user_input = input("You: ").strip()
            if not user_input:
                continue

            result = process_onboarding_answer(USER_ID, user_input)

            if result["done"]:
                agent_name = result.get("agent_name", "Buddy")
                user_name = result.get("user_name", "friend")
                print(f"\n{agent_name}: Set. I'm {agent_name}. Talk to me whenever, {user_name}.")
                print(f"{agent_name}: Type /help to see what I can do.\n")
                break
            else:
                step = result["step"]
                total = result["total"]
                print(f"\n[{step}/{total}] {result['next_question']}\n")

    profile = get_profile(USER_ID)
    agent_name = profile.get("agent_name", "Buddy")
    user_name = profile.get("user_name", "friend")

    print(f"\n{agent_name} is ready. Type /help for commands, /quit to exit.\n")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{agent_name}: Later.")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            print(f"{agent_name}: Later.")
            break

        if user_input == "/help":
            print(f"\n{get_help_text().replace('*', '').replace('`', '')}\n")
            continue

        if user_input == "/forget":
            confirm = input("Wipe all memory? (yes/no): ")
            if confirm.lower() == "yes":
                clear_user(USER_ID)
                print("Memory wiped. Restart to set up again.")
                break
            continue

        # Check skill triggers dynamically
        skill_prompt = None
        clean_text = user_input
        all_skills = get_all_skills()
        
        for skill_name, skill in all_skills.items():
            trigger = skill.get("trigger")
            if trigger and user_input.startswith(trigger) and not skill.get("system"):
                skill_prompt = get_skill_prompt(trigger)
                clean_text = user_input[len(trigger):].strip()
                if not clean_text:
                    clean_text = f"User triggered {trigger} — ask what they want."
                break

        message = f"[SKILL: {skill_prompt}]\n\n{clean_text}" if skill_prompt else user_input

        # Chat and handle results (including recursive tool confirmation)
        result = await chat(USER_ID, message)
        
        while "action_required" in result:
            action_req = result["action_required"]
            action_id = action_req["action_id"]
            
            pending = get_pending_action(action_id)
            if not pending:
                print(f"\n{agent_name}: Action expired.")
                break

            print(f"\n{agent_name}: [SECURITY] {action_req['display']}")
            confirm = input("Confirm? (y/n): ").strip().lower()
            
            if confirm == 'y':
                result = await chat(USER_ID, pending["message"], confirmed_action=pending["action"])
                delete_pending_action(action_id)
            else:
                delete_pending_action(action_id)
                print(f"{agent_name}: Action cancelled.")
                result = {"reply": "I cancelled the action as requested."}
                break

        reply = result.get("reply", "No response.")
        print(f"\n{agent_name}: {reply}\n")


def run_cli():
    asyncio.run(cli_chat())
