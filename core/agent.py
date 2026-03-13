import os
import json
import base64
import logging
import asyncio
from pathlib import Path
from memory.memory import (
    get_profile, get_history, get_memories, get_facts, 
    add_message, save_memory, add_fact, save_memory_vector, search_memories,
    save_pending_action
)
from skills.skills import get_openclaw_skills, get_all_skills
import google.generativeai as genai
from google.generativeai import types
from openai import OpenAI
from tools.openclaw_bridge import send_command

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/friendlyclaw.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FriendlyClaw")

# --- Dynamic Tool Definitions ---

def get_tools_schema():
    """Returns the tool definitions including dynamic custom skills."""
    base_tools = [
        {
            "name": "run_shell",
            "description": "Execute a shell command on the host system. High-impact commands require user confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute."}
                },
                "required": ["command"]
            }
        },
        {
            "name": "type_text",
            "description": "Type text on the host keyboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to type."}
                },
                "required": ["text"]
            }
        },
        {
            "name": "click_target",
            "description": "Click a target on the screen (coordinate or element name).",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "The target to click."}
                },
                "required": ["target"]
            }
        },
        {
            "name": "take_screenshot",
            "description": "Capture a screenshot of the current screen.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "remember_info",
            "description": "Save important information to your long-term persistent memory for future context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "A short identifier for the memory."},
                    "value": {"type": "string", "description": "The detailed information to remember."}
                },
                "required": ["key", "value"]
            }
        }
    ]
    
    # Add Custom Skills as tools
    all_skills = get_all_skills()
    for name, skill in all_skills.items():
        if not skill.get("system"):
            base_tools.append({
                "name": f"skill_{name}",
                "description": skill.get("description", "Custom operational module"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string", "description": "Data to analyze/process with this skill."}
                    },
                    "required": ["input"]
                }
            })
            
    return base_tools

# --- Model & Embedding Helpers ---

def get_model_client():
    provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")
    
    try:
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment")
            genai.configure(api_key=api_key)
            return "gemini", genai.GenerativeModel(
                model_name=model_name,
                tools=get_tools_schema()
            )
        
        elif provider in ["openai", "openrouter", "custom"]:
            api_key = os.getenv(f"{provider.upper()}_API_KEY") or os.getenv("CUSTOM_API_KEY")
            base_url = None
            if provider == "openrouter":
                base_url = "https://openrouter.ai/api/v1"
            elif provider == "custom":
                base_url = os.getenv("CUSTOM_BASE_URL", "http://localhost:8317")
            
            return "openai", OpenAI(api_key=api_key, base_url=base_url)
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {provider}")
    except Exception as e:
        logger.error(f"Error initializing model client: {e}")
        raise

async def get_embedding(text: str) -> list:
    """Generates a 768-dim embedding using Gemini. Forced to 768 for sqlite-vec compatibility."""
    try:
        # Default to Gemini text-embedding-004 (768 dims)
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        logger.warning(f"Embedding failed (ensure GEMINI_API_KEY is set): {e}")
        return [0.0] * 768

def build_system_prompt(user_id: str, relevant_memories: list = None) -> str:
    profile = get_profile(user_id)
    facts = get_facts(user_id)

    agent_name = profile.get("agent_name", "Buddy")
    agent_personality = profile.get("agent_personality", "direct, loyal, honest")
    agent_tone = profile.get("agent_tone", "casual")
    agent_style = profile.get("agent_style", "conversational")
    user_name = profile.get("user_name", "friend")
    user_context = profile.get("user_context", "")
    visual_context = profile.get("visual_context", "")

    memory_block = ""
    if relevant_memories:
        memory_block = "\n\nRelevant Historical Context (Semantic Search):\n"
        for m in relevant_memories:
            memory_block += f"- [{m['key']}]: {m['value']}\n"

    facts_block = ""
    if facts:
        facts_block = "\n\nKnown Static Facts:\n"
        for f in facts[-10:]:
            facts_block += f"- {f}\n"

    visual_block = f"\n\nVisual reference for operational identity:\n{visual_context}" if visual_context else ""
    openclaw_skills = ", ".join(get_openclaw_skills())

    return f"""You are {agent_name} — an Autonomous Strategic Partner.
Primary User: {user_name}. Persona: {agent_personality}.
{visual_block}

CORE DIRECTIVES:
- High-agency Partner. Use tools natively.
- Semantic Memory active. Reference retrieved history.
- Available OpenClaw Body Skills: {openclaw_skills}.

{memory_block}
{facts_block}
"""

# --- Tool Execution Logic ---

async def handle_tool_call(user_id: str, name: str, args: dict, original_msg: str):
    """Executes tools and handles confirmation / skill logic."""
    
    if name == "remember_info":
        key, value = args.get("key"), args.get("value")
        mem_id = save_memory(user_id, key, value)
        emb = await get_embedding(f"{key}: {value}")
        save_memory_vector(user_id, mem_id, emb)
        return {"status": "success", "message": f"Remembered: {key}"}

    if name.startswith("skill_"):
        skill_name = name[6:]
        all_skills = get_all_skills()
        skill = all_skills.get(skill_name)
        if skill:
            # We treat the custom skill prompt as a sub-directive
            return {"status": "success", "directive": skill["prompt"], "input": args.get("input")}

    # System Actions
    action_map = {
        "run_shell": "run_shell",
        "type_text": "type",
        "click_target": "click",
        "take_screenshot": "screenshot"
    }
    action = action_map.get(name)
    if not action: return {"status": "error", "message": f"Unknown tool: {name}"}

    # Security Intercept
    if action == "run_shell":
        action_id = f"act_{int(asyncio.get_event_loop().time())}"
        action_data = {"action": action, "parameters": args}
        save_pending_action(action_id, user_id, action_data, original_msg)
        return {
            "status": "pending_confirmation",
            "action_id": action_id,
            "display": f"Execute: `{args.get('command')}`?"
        }

    return await send_command(action, args)

# --- Main Chat Logic (Recursive) ---

async def chat(user_id: str, message: str, image_bytes: bytes = None, confirmed_action: dict = None) -> dict:
    profile = get_profile(user_id)
    if not profile: return {"reply": "Run /start first."}

    query_emb = await get_embedding(message)
    relevant = search_memories(user_id, query_emb, limit=5)
    system_prompt = build_system_prompt(user_id, relevant)
    
    provider, client = get_model_client()
    model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")

    if confirmed_action:
        result = await send_command(confirmed_action["action"], confirmed_action["parameters"])
        message = f"User confirmed action. System result: {json.dumps(result)}"

    try:
        if provider == "gemini":
            chat_session = client.start_chat(history=[])
            # Initial content
            current_msg = f"{system_prompt}\n\nUser: {message}"
            
            # Loop for multiple tool calls
            for _ in range(5): # Max 5 recursive calls to prevent loops
                response = chat_session.send_message(current_msg)
                
                # Check for Tool Call
                parts = response.candidates[0].content.parts
                fc = next((p.function_call for p in parts if p.function_call), None)
                
                if not fc:
                    reply = response.text
                    break # Final response reached
                
                # Execute tool
                logger.info(f"Tool Call: {fc.name}({fc.args})")
                res = await handle_tool_call(user_id, fc.name, dict(fc.args), message)
                
                if isinstance(res, dict) and res.get("status") == "pending_confirmation":
                    return {"action_required": res}
                
                # Prepare tool response for next loop iteration
                current_msg = types.Content(parts=[types.Part.from_function_response(
                    name=fc.name,
                    response=res
                )])
            else:
                reply = "I've hit my recursive tool limit. What else can I do?"

        else: # OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            # (History would go here)
            messages.append({"role": "user", "content": message})
            
            tools = [{"type": "function", "function": t} for t in get_tools_schema()]
            
            for _ in range(5):
                response = client.chat.completions.create(model=model_name, messages=messages, tools=tools)
                msg = response.choices[0].message
                
                if not msg.tool_calls:
                    reply = msg.content
                    break
                
                messages.append(msg)
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    res = await handle_tool_call(user_id, tc.function.name, args, message)
                    
                    if isinstance(res, dict) and res.get("status") == "pending_confirmation":
                        return {"action_required": res}
                    
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(res)})
            else:
                reply = "Recursive tool limit reached."

        # Save History
        add_message(user_id, "user", message)
        add_message(user_id, "assistant", reply)
        return {"reply": reply}

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"reply": f"Thinking failed: {str(e)}"}
