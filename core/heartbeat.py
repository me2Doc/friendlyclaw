import os
import time
import logging
import asyncio
from pathlib import Path

logger = logging.getLogger("FriendlyClaw.Heartbeat")

HEARTBEAT_FILE = Path("HEARTBEAT.md")
USER_ID = "cli_user" # Default user for background heartbeats

async def trigger_heartbeat():
    """Reads HEARTBEAT.md and triggers a proactive AI turn."""
    from core.agent import chat
    
    if not HEARTBEAT_FILE.exists():
        return

    try:
        with open(HEARTBEAT_FILE, "r") as f:
            missions = f.read()
            
        logger.info("💓 Triggering Heartbeat Mission...")
        
        # We use a special prefix to put the AI in 'Sentinel Mode'
        prompt = f"[HEARTBEAT MISSION] Here are my current background objectives:\n\n{missions}\n\nPerform a quick audit of these objectives. Use tools if necessary. If everything is normal, do not notify the user. If an anomaly is detected, provide a brief alert."
        
        result = await chat(USER_ID, prompt)
        
        # If the AI has a reply that isn't just 'normal', we might want to notify the platform
        # For now, we just log it. The chat function already handles platform output if needed.
        logger.info(f"Heartbeat Result: {result.get('reply', 'No findings.')}")
        
    except Exception as e:
        logger.error(f"Heartbeat failed: {e}")

def heartbeat_loop(interval_minutes=15):
    """Background loop for the heartbeat."""
    print(f"💓 Heartbeat Monitor active (every {interval_minutes}m).")
    while True:
        # We run the async trigger in the loop
        asyncio.run(trigger_heartbeat())
        time.sleep(interval_minutes * 60)
