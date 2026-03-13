import os
import json
import base64
import logging
import asyncio
from pathlib import Path
from brain.memory.memory import (
    get_profile, get_history, get_memories, get_facts, 
    add_message, save_memory, add_fact, save_memory_vector, search_memories,
    save_pending_action, add_task, update_task, get_user_tasks, get_task, add_audit_log
)
from brain.skills.skills import get_openclaw_skills, get_all_skills
import google.generativeai as genai
from google.generativeai import types
from openai import OpenAI
from brain.tools.openclaw_bridge import send_command
from brain.tools.web_intelligence import deep_read_url
from brain.core.scheduler import schedule_mission, list_missions
from brain.core.swarm import swarm
from brain.core.prompts import MODE_DIRECTIVE_SENTINEL

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

# --- Security & Sandboxing ---

def is_path_safe(command: str) -> bool:
    """
    Checks if a command attempts to escape the WORKSPACE_ROOT.
    This is a 'Sandbox Lite' implementation.
    """
    workspace_root = os.getenv("WORKSPACE_ROOT")
    if not workspace_root:
        return True # If not set, we assume the user allows full access (Standard Mode)

    root = Path(workspace_root).resolve()
    # Simple check for common escape patterns
    dangerous_patterns = ["../", "/etc", "/root", "/var/log", "/home/me2doc/.ssh"]
    for pattern in dangerous_patterns:
        if pattern in command:
            return False
    return True

# --- Dynamic Tool Definitions ---

def get_tools_schema():
    """Returns the tool definitions including dynamic custom skills."""
    base_tools = [
        {
            "name": "spawn_subagent",
            "description": "Delegate a complex or long-running task to a background sub-agent (Ghost Worker). Use this for deep research, data gathering, or heavy tasks that shouldn't block the main chat.",
            "parameters": {
                "type": "object",
                "properties": {
                    "objective": {"type": "string", "description": "The specific goal for the sub-agent to achieve."}
                },
                "required": ["objective"]
            }
        },
        {
            "name": "list_active_tasks",
            "description": "View the status of all background missions and sub-agent tasks (The Strategic Task Board).",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "synthesize_task",
            "description": "Retrieve and summarize the results of a completed background task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to synthesize."}
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "visual_pulse",
            "description": "Perform a visual audit of the current environment. Tries camera snapshot first, then falls back to desktop screenshot.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "schedule_mission",
            "description": "Schedule a proactive mission (AI prompt) to run at a specific time using a cron expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cron": {"type": "string", "description": "Standard 5-field cron (min hour day month dow)."},
                    "mission_prompt": {"type": "string", "description": "The strategic instruction for the AI."}
                },
                "required": ["cron", "mission_prompt"]
            }
        },
        {
            "name": "deep_read_url",
            "description": "Perform a deep, clean read of a specific URL to extract its main content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The full URL to read."}
                },
                "required": ["url"]
            }
        },
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
            "description": "Click a target on the screen.",
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
            "description": "Save important information to your long-term persistent memory.",
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
    model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            return "gemini", genai.GenerativeModel(model_name=model_name, tools=get_tools_schema())
        except Exception as e: logger.warning(f"Gemini init failed: {e}")

    or_key = os.getenv("OPENROUTER_API_KEY")
    if or_key:
        try: return "openai", OpenAI(api_key=or_key, base_url="https://openrouter.ai/api/v1")
        except Exception as e: logger.warning(f"OpenRouter init failed: {e}")

    oa_key = os.getenv("OPENAI_API_KEY")
    if oa_key:
        try: return "openai", OpenAI(api_key=oa_key)
        except Exception as e: logger.warning(f"OpenAI init failed: {e}")

    custom_url = os.getenv("CUSTOM_BASE_URL", "http://localhost:8317")
    return "openai", OpenAI(api_key=os.getenv("CUSTOM_API_KEY", "fake"), base_url=custom_url)

async def get_embedding(text: str) -> list:
    try:
        result = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
        return result['embedding']
    except Exception as e:
        return [0.0] * 768

def build_system_prompt(user_id: str, relevant_memories: list = None, is_heartbeat: bool = False) -> str:
    profile = get_profile(user_id)
    facts = get_facts(user_id)
    agent_name = profile.get("agent_name", "Buddy")
    agent_personality = profile.get("agent_personality", "direct, loyal, honest")
    user_name = profile.get("user_name", "friend")
    visual_context = profile.get("visual_context", "")

    memory_block = ""
    if relevant_memories:
        memory_block = "\n\nRelevant Historical Context (Semantic Search):\n"
        for m in relevant_memories: memory_block += f"- [{m['key']}]: {m['value']}\n"

    facts_block = ""
    if facts:
        facts_block = "\n\nKnown Static Facts:\n"
        for f in facts[-10:]: facts_block += f"- {f}\n"

    visual_block = f"\n\nVisual reference for operational identity:\n{visual_context}" if visual_context else ""
    openclaw_skills = ", ".join(get_openclaw_skills())
    mode_directive = MODE_DIRECTIVE_SENTINEL if is_heartbeat else ""

    return f"""You are {agent_name} — an Autonomous Strategic Partner.
Primary User: {user_name}. Persona: {agent_personality}.{mode_directive}
{visual_block}

CORE DIRECTIVES:
- High-agency Partner. Use tools natively.
- Semantic Memory active. Reference retrieved history.
- Swarm Capability: You can delegate tasks to background sub-agents using 'spawn_subagent'.
- Persistent Task Board: Track missions with 'list_active_tasks'.

Available Body Skills: {openclaw_skills}.

{memory_block}
{facts_block}
"""

# --- Tool Execution Logic ---

async def handle_tool_call(user_id: str, name: str, args: dict, original_msg: str):
    # Swarm Tools
    if name == "spawn_subagent":
        objective = args.get("objective")
        task_id = add_task(user_id, objective)
        swarm.spawn(user_id, task_id, objective)
        return {"status": "success", "message": f"Sub-agent spawned. Task ID: #{task_id}.", "task_id": task_id}

    if name == "list_active_tasks":
        return {"status": "success", "tasks": get_user_tasks(user_id)}

    if name == "synthesize_task":
        task_id = args.get("task_id")
        task = get_task(task_id)
        if task:
            # If task was a sub-agent worker, we could pull its full conversation history here if we wanted
            return {"status": "success", "objective": task["objective"], "status": task["status"], "result": task["result"]}
        return {"status": "error", "message": "Task not found."}

    # Intelligence Tools
    if name == "visual_pulse":
        try:
            cam_res = await send_command("camsnap", {"action": "snap", "parameters": {"out": "data/pulse.jpg"}})
            if cam_res.get("status") == "success": return {"status": "success", "observation": "Camera snapshot captured."}
        except: pass
        return await send_command("screenshot", {})

    if name == "schedule_mission":
        return schedule_mission(user_id, args.get("cron"), args.get("mission_prompt"))

    if name == "deep_read_url":
        return {"status": "success", "content": deep_read_url(args.get("url"))}

    if name == "remember_info":
        key, value = args.get("key"), args.get("value")
        mem_id = save_memory(user_id, key, value)
        emb = await get_embedding(f"{key}: {value}")
        save_memory_vector(user_id, mem_id, emb)
        return {"status": "success", "message": f"Remembered: {key}"}

    if name.startswith("skill_"):
        skill_name = name[6:]
        skill = get_all_skills().get(skill_name)
        if skill: return {"status": "success", "directive": skill["prompt"], "input": args.get("input")}

    # System Actions (with Audit Log & Sandbox)
    action_map = {"run_shell": "run_shell", "type_text": "type", "click_target": "click", "take_screenshot": "screenshot"}
    action = action_map.get(name)
    if not action: return {"status": "error", "message": f"Unknown tool: {name}"}

    if action == "run_shell":
        command = args.get("command", "")
        if not is_path_safe(command):
            return {"status": "error", "message": "Access Denied: Command attempts to access files outside WORKSPACE_ROOT."}

        action_id = f"act_{int(asyncio.get_event_loop().time())}"
        save_pending_action(action_id, user_id, {"action": action, "parameters": args}, original_msg)
        return {"status": "pending_confirmation", "action_id": action_id, "display": f"Execute: `{command}`?"}

    result = await send_command(action, args)
    # Log system actions to audit trail
    if action == "run_shell" and result.get("status") == "success":
        add_audit_log(user_id, args.get("command"), str(result.get("output")))
    
    return result

# --- Main Chat Logic (Recursive) ---

async def chat(user_id: str, message: str, image_bytes: bytes = None, confirmed_action: dict = None) -> dict:
    profile = get_profile(user_id)
    # Background workers use worker_ profile which might not exist, we use fallback
    if not profile and not user_id.startswith("worker_"): 
        return {"reply": "Run /start first."}
    if not profile:
        profile = {"agent_name": "Ghost-Worker", "user_name": "System"}

    is_heartbeat = "[HEARTBEAT MISSION]" in message
    query_emb = await get_embedding(message)
    relevant = search_memories(user_id, query_emb, limit=5)
    system_prompt = build_system_prompt(user_id, relevant, is_heartbeat=is_heartbeat)
    
    provider, client = get_model_client()
    model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")

    if confirmed_action:
        result = await send_command(confirmed_action["action"], confirmed_action["parameters"])
        if confirmed_action["action"] == "run_shell":
            add_audit_log(user_id, confirmed_action["parameters"].get("command"), str(result.get("output")))
        message = f"User confirmed action. System result: {json.dumps(result)}"

    try:
        if provider == "gemini":
            chat_session = client.start_chat(history=[])
            current_msg = f"{system_prompt}\n\nUser: {message}"
            for _ in range(5): 
                response = chat_session.send_message(current_msg)
                parts = response.candidates[0].content.parts
                fc = next((p.function_call for p in parts if p.function_call), None)
                if not fc:
                    reply = response.text
                    break 
                res = await handle_tool_call(user_id, fc.name, dict(fc.args), message)
                if isinstance(res, dict) and res.get("status") == "pending_confirmation":
                    return {"action_required": res}
                current_msg = types.Content(parts=[types.Part.from_function_response(name=fc.name, response=res)])
            else: reply = "Recursive tool limit reached."

        else: # OpenAI
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
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
            else: reply = "Recursive tool limit reached."

        add_message(user_id, "user", message)
        add_message(user_id, "assistant", reply)
        return {"reply": reply}

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"reply": f"Thinking failed: {str(e)}"}
