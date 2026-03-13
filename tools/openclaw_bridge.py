import os
import json
import logging
import asyncio
import websockets

logger = logging.getLogger("FriendlyClaw.OpenClaw")

OPENCLAW_URL = os.getenv("OPENCLAW_WS_URL", "ws://127.0.0.1:18789")

# HARD SECURITY: Prohibited command patterns that will be blocked before transmission.
COMMAND_BLACKLIST = [
    "rm -rf /", "rm -rf *", "mkfs", "dd if=", "> /dev/sd", 
    "chmod -R 777", "chown -R", ":(){", "shutdown", "reboot"
]

async def check_gateway_health(timeout=30) -> bool:
    """
    Polls the OpenClaw gateway until it responds or the timeout is reached.
    """
    logger.info(f"Checking OpenClaw Gateway health at {OPENCLAW_URL}...")
    start_time = asyncio.get_event_loop().time()
    
    while True:
        try:
            async with websockets.connect(OPENCLAW_URL, ping_interval=None) as websocket:
                logger.info("OpenClaw Gateway is online and ready.")
                return True
        except (ConnectionRefusedError, OSError):
            if asyncio.get_event_loop().time() - start_time > timeout:
                logger.error(f"Gateway failed to come online within {timeout} seconds.")
                return False
            await asyncio.sleep(1)

async def send_command(action: str, parameters: dict = None) -> dict:
    """
    Sends a command to the OpenClaw Gateway via WebSocket.
    Includes hard security validation for shell commands.
    """
    if parameters is None:
        parameters = {}

    # SECURITY VALIDATION
    if action == "run_shell" and "command" in parameters:
        cmd = parameters["command"].lower()
        for blocked in COMMAND_BLACKLIST:
            if blocked in cmd:
                logger.warning(f"SECURITY ALERT: Blocked attempted destructive command: {cmd}")
                return {"status": "error", "message": f"Security violation: Command '{blocked}' is prohibited."}
        
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