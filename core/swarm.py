import os
import logging
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from memory.memory import update_task, add_message
from core.prompts import SWARM_SUBAGENT_PROMPT

logger = logging.getLogger("FriendlyClaw.Swarm")

class SwarmManager:
    _instance = None
    _executor = ThreadPoolExecutor(max_workers=5)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SwarmManager, cls).__new__(cls)
        return cls._instance

    def spawn(self, user_id: str, task_id: int, objective: str):
        """Spawns a background worker for a specific task."""
        logger.info(f"🐝 Swarm spawning worker for task {task_id}: {objective[:50]}...")
        self._executor.submit(self._run_worker, user_id, task_id, objective)

    def _run_worker(self, user_id: str, task_id: int, objective: str):
        """Internal worker logic running in a thread with its own event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._async_worker(user_id, task_id, objective))
        finally:
            loop.close()

    async def _async_worker(self, user_id: str, task_id: int, objective: str):
        """Asynchronous part of the worker."""
        from core.agent import chat
        
        update_task(task_id, "running")
        
        try:
            # Sub-agents use a specialized 'Mission' prompt from core.prompts
            prompt = SWARM_SUBAGENT_PROMPT.format(objective=objective)
            
            result = await chat(user_id, prompt)
            reply = result.get("reply", "No result provided.")
            
            update_task(task_id, "completed", reply)
            logger.info(f"✅ Swarm task {task_id} completed.")
            
            # Trigger notification
            await self._notify_completion(user_id, task_id, objective, reply)
            
        except Exception as e:
            logger.error(f"❌ Swarm task {task_id} failed: {e}")
            update_task(task_id, "failed", str(e))

    async def _notify_completion(self, user_id: str, task_id: int, objective: str, result: str):
        """Notifies the user that a background task is done."""
        platform = os.getenv("PLATFORM", "cli").lower()
        
        text = f"🐝 *Swarm Update*\nTask #{task_id} Completed.\n\n*Objective:* {objective}\n\nUse `/synthesize {task_id}` to read the full report."
        
        if platform == "telegram":
            try:
                from telegram import Bot
                token = os.getenv("TELEGRAM_BOT_TOKEN")
                if token:
                    bot = Bot(token)
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"Failed to send Telegram notification: {e}")
        else:
            print(f"\n\n[SWARM] Task #{task_id} Completed: {objective}\n")

# Global singleton
swarm = SwarmManager()
