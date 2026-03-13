import os
import logging
import asyncio
import traceback
from concurrent.futures import ThreadPoolExecutor
from brain.memory.memory import update_task, add_message
from brain.core.prompts import SWARM_SUBAGENT_PROMPT

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
        from brain.core.agent import chat
        
        # SCOPED CONTEXT: Sub-agents use 'worker_{task_id}' to isolate their thinking
        worker_context_id = f"worker_{task_id}"
        
        update_task(task_id, "running")
        
        try:
            # Sub-agents use a specialized 'Mission' prompt from brain.core.prompts
            prompt = SWARM_SUBAGENT_PROMPT.format(objective=objective)
            
            # Sub-agent turn with isolated ID
            result = await chat(worker_context_id, prompt)
            reply = result.get("reply", "No result provided.")
            
            update_task(task_id, "completed", reply)
            logger.info(f"✅ Swarm task {task_id} completed.")
            
            # Trigger notification to the ORIGINAL user_id
            await self._notify_completion(user_id, task_id, objective, reply)
            
        except Exception as e:
            error_detail = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            logger.error(f"❌ Swarm task {task_id} failed: {e}")
            update_task(task_id, "failed", error_detail)

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
