import os
import json
import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlite import SQLAlchemyJobStore
from memory.memory import DB_PATH

logger = logging.getLogger("FriendlyClaw.Scheduler")

# Global scheduler instance
_scheduler = None

def get_scheduler():
    global _scheduler
    if _scheduler is None:
        jobstores = {
            'default': SQLAlchemyJobStore(url=f'sqlite:///{DB_PATH}')
        }
        _scheduler = AsyncIOScheduler(jobstores=jobstores)
    return _scheduler

async def run_mission(user_id: str, prompt: str):
    """Executes a scheduled mission (AI prompt)."""
    from core.agent import chat
    logger.info(f"Executing scheduled mission for {user_id}: {prompt[:50]}...")
    
    try:
        # Run the mission through the agent
        result = await chat(user_id, f"[SCHEDULED MISSION] {prompt}")
        reply = result.get("reply", "Mission completed with no output.")
        
        # Determine platform to send notification
        platform = os.getenv("PLATFORM", "cli").lower()
        
        if platform == "telegram":
            # We need to import the bot to send message
            from telegram import Bot
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            if token:
                bot = Bot(token)
                await bot.send_message(
                    chat_id=user_id,
                    text=f"📋 *Mission Report*\n\n{reply}",
                    parse_mode="Markdown"
                )
        else:
            print(f"\n📋 MISSION REPORT ({datetime.now().strftime('%H:%M')}):\n{reply}\n")
            
    except Exception as e:
        logger.error(f"Mission failed: {e}")

def schedule_mission(user_id: str, cron_expression: str, prompt: str):
    """Schedules a new mission using a cron expression."""
    scheduler = get_scheduler()
    job_id = f"mission_{user_id}_{int(datetime.now().timestamp())}"
    
    try:
        scheduler.add_job(
            run_mission,
            'cron',
            args=[user_id, prompt],
            id=job_id,
            replace_existing=True,
            **parse_cron(cron_expression)
        )
        return {"status": "success", "job_id": job_id}
    except Exception as e:
        logger.error(f"Failed to schedule mission: {e}")
        return {"status": "error", "message": str(e)}

def parse_cron(cron_str: str) -> dict:
    """Simple parser for standard cron (5 fields)."""
    fields = cron_str.split()
    if len(fields) != 5:
        raise ValueError("Cron expression must have 5 fields (min hour day month dow)")
        
    return {
        "minute": fields[0],
        "hour": fields[1],
        "day": fields[2],
        "month": fields[3],
        "day_of_week": fields[4]
    }

def list_missions(user_id: str):
    """Lists all scheduled missions for a user."""
    scheduler = get_scheduler()
    jobs = scheduler.get_jobs()
    user_jobs = []
    for job in jobs:
        if job.id.startswith(f"mission_{user_id}"):
            user_jobs.append({
                "id": job.id,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else "Paused",
                "prompt": job.args[1]
            })
    return user_jobs

def start_scheduler():
    """Initializes and starts the global scheduler."""
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.start()
        logger.info("Strategic Mission Scheduler started.")
