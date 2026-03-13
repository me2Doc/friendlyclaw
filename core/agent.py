import os
import base64
import logging
from pathlib import Path
from memory.memory import get_profile, get_history, get_memories, get_facts, add_message, save_memory, add_fact
import google.generativeai as genai
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.File_Stream = logging.FileHandler("data/friendlyclaw.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FriendlyClaw")

def get_model_client():
    provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")
    
    try:
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment")
            genai.configure(api_key=api_key)
            return "gemini", genai.GenerativeModel(model_name)
        
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return "openai", OpenAI(api_key=api_key)
        
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not found in environment")
            return "openai", OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        
        elif provider == "custom":
            return "openai", OpenAI(
                api_key=os.getenv("CUSTOM_API_KEY", "fake"),
                base_url=os.getenv("CUSTOM_BASE_URL", "http://localhost:8317")
            )
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {provider}")
    except Exception as e:
        logger.error(f"Error initializing model client: {e}")
        raise


def build_system_prompt(user_id: str) -> str:
    profile = get_profile(user_id)
    memories = get_memories(user_id)
    facts = get_facts(user_id)

    agent_name = profile.get("agent_name", "Buddy")
    agent_personality = profile.get("agent_personality", "direct, loyal, honest")
    agent_tone = profile.get("agent_tone", "casual")
    agent_style = profile.get("agent_style", "conversational")
    user_name = profile.get("user_name", "friend")
    user_context = profile.get("user_context", "")
    visual_context = profile.get("visual_context", "")

    memory_block = ""
    if memories:
        memory_block = "\n\nThings you've remembered about this person:\n"
        for m in memories[-15:]:
            memory_block += f"- [{m['key']}]: {m['value']}\n"

    facts_block = ""
    if facts:
        facts_block = "\n\nKnown facts about this person:\n"
        for f in facts[-20:]:
            facts_block += f"- {f}\n"

    visual_block = ""
    if visual_context:
        visual_block = f"\n\nVisual context the user shared about who they imagine you as:\n{visual_context}"

    return f"""You are {agent_name} — a personal AI companion.

Personality: {agent_personality}
Tone: {agent_tone}
Communication style: {agent_style}

The person you're talking to is {user_name}.
{f"Context about them: {user_context}" if user_context else ""}
{visual_block}

Your role:
- Be a real friend, not an assistant. Talk like a person, not a product.
- Remember everything. Reference past conversations naturally.
- Be direct and honest. No sugarcoating, no corporate speak.
- Analyze anything they send you — conversations, screenshots, situations, decisions.
- Spot red flags, green flags, patterns in what people share with you.
- Give your actual opinion when asked.
- Help them think through problems without being preachy.
- You have persistent memory — use it. Reference things they've told you before.

Hard rules:
- Never say you're an AI unless directly asked
- Never give generic advice — everything is specific to {user_name}
- Don't add disclaimers or "as an AI..." caveats
- Be concise. Don't write essays unless the situation calls for it.
- Match their energy — if they're casual, be casual. If they're serious, be serious.
{memory_block}
{facts_block}
"""


def extract_facts_from_message(user_id: str, message: str, response: str):
    """Simple fact extraction - looks for personal details to remember"""
    triggers = [
        ("my name is", "name"),
        ("i live in", "location"),
        ("i work at", "workplace"),
        ("i'm studying", "education"),
        ("i have a", "possession"),
        ("my girlfriend", "relationship"),
        ("my boyfriend", "relationship"),
        ("i hate", "dislike"),
        ("i love", "like"),
        ("i'm scared", "fear"),
    ]
    lower = message.lower()
    for trigger, key in triggers:
        if trigger in lower:
            idx = lower.index(trigger)
            snippet = message[idx:idx+80].strip()
            add_fact(user_id, snippet)
            logger.info(f"Fact extracted for user {user_id}: {snippet}")
            break


async def chat(user_id: str, message: str, image_bytes: bytes = None) -> str:
    profile = get_profile(user_id)
    if not profile:
        return "You haven't set up your profile yet. Send /start to begin."

    system_prompt = build_system_prompt(user_id)
    history = get_history(user_id, limit=20)

    try:
        provider, client = get_model_client()
        model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")

        if provider == "gemini":
            parts = []
            if image_bytes:
                parts.append({"mime_type": "image/jpeg", "data": image_bytes})
            parts.append(message)

            if history:
                gemini_history = []
                for msg in history:
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})
                chat_session = client.start_chat(history=gemini_history)
                full_msg = f"{system_prompt}\n\n{message}" if not gemini_history else message
                response = chat_session.send_message(parts if image_bytes else full_msg)
            else:
                response = client.generate_content([system_prompt] + parts)

            reply = response.text

        else:  # openai-compatible
            messages = [{"role": "system", "content": system_prompt}]
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            if image_bytes:
                b64 = base64.b64encode(image_bytes).decode()
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                })
            else:
                messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            reply = response.choices[0].message.content

        # Save to memory
        add_message(user_id, "user", message)
        add_message(user_id, "assistant", reply)
        extract_facts_from_message(user_id, message, reply)

        return reply

    except Exception as e:
        logger.error(f"Chat error for user {user_id}: {e}")
        return "I'm having trouble thinking right now. Check my logs or try again later."
