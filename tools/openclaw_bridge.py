import os
import json
import logging
import asyncio
import websockets

logger = logging.getLogger("FriendlyClaw.OpenClaw")

OPENCLAW_URL = os.getenv("OPENCLAW_WS_URL", "ws://127.0.0.1:18789")

async def send_command(action: str, parameters: dict = None) -> dict:
    """
    Sends a command to the OpenClaw Gateway via WebSocket.
    """
    if parameters is None:
        parameters = {}
        
    payload = {
        "action": action,
        "parameters": parameters
    }
    
    try:
        async with websockets.connect(OPENCLAW_URL, ping_interval=None) as websocket:
            logger.info(f"Sending to OpenClaw: {payload}")
            await websocket.send(json.dumps(payload))
            
            response = await websocket.recv()
            logger.info(f"Received from OpenClaw: {response}")
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"status": "success", "raw": response}
                
    except ConnectionRefusedError:
        logger.error(f"Could not connect to OpenClaw at {OPENCLAW_URL}. Is it running?")
        return {"status": "error", "message": "OpenClaw is not running or unreachable."}
    except Exception as e:
        logger.error(f"OpenClaw communication error: {e}")
        return {"status": "error", "message": str(e)}

# Exposed Tool Definition for LLMs
OPENCLAW_TOOL_SCHEMA = {
    "name": "openclaw_execute",
    "description": "Execute system-level actions like moving the mouse, typing, or opening apps via OpenClaw.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "The command to execute (e.g., 'click', 'type', 'screenshot', 'run_shell')."
            },
            "parameters": {
                "type": "object",
                "description": "Key-value pairs required for the action (e.g., {'text': 'hello'} for typing)."
            }
        },
        "required": ["action"]
    }
}
