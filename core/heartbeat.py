import os
import time
import logging
import asyncio
from pathlib import Path
from core.prompts import HEARTBEAT_SENTINEL_PROMPT

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
        
        # We use a specialized prompt from core.prompts
        prompt = HEARTBEAT_SENTINEL_PROMPT.format(missions=missions)
        
        result = await chat(USER_ID, prompt)
        logger.info(f"Heartbeat Result: {result.get('reply', 'No findings.')}")
        
    except Exception as e:
        logger.error(f"Heartbeat failed: {e}")

def heartbeat_loop(interval_minutes=15):
    """Background loop for the heartbeat with robust event loop handling."""
    print(f"💓 Heartbeat Monitor active (every {interval_minutes}m).")
    while True:
        # Create a new loop for each heartbeat turn to be safe in a background thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(trigger_heartbeat())
        finally:
            loop.close()
        time.sleep(interval_minutes * 60)
