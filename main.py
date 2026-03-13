import os
import sys
import subprocess
import asyncio
import threading
import time
from dotenv import load_dotenv
from brain.memory.memory import init_db
from brain.tools.openclaw_bridge import check_gateway_health
from brain.tools.config_sync import sync_openclaw_config
from brain.core.scheduler import start_scheduler
from brain.core.heartbeat import heartbeat_loop

load_dotenv()
init_db()

# Global to track the gateway process
gateway_process = None

def start_openclaw_gateway():
    """Starts the OpenClaw gateway in the background if it's not already running."""
    global gateway_process
    
    # Ensure body config is synced with .env first
    sync_openclaw_config()
    
    gateway_script = os.path.join(os.getcwd(), "body", "openclaw.mjs")
    if not os.path.exists(gateway_script):
        print("Warning: OpenClaw gateway script (body/openclaw.mjs) not found.")
        return None

    print("🚀 Starting OpenClaw Gateway (System Body)...")
    try:
        # Start gateway in background
        gateway_process = subprocess.Popen(
            ["node", gateway_script, "gateway"],
            cwd=os.path.join(os.getcwd(), "body"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for the gateway to become healthy
        is_up = asyncio.run(check_gateway_health(timeout=30))
        if not is_up:
            print("⚠️ Warning: Gateway did not become healthy in time.")
            
        return gateway_process
    except Exception as e:
        print(f"Error starting OpenClaw gateway: {e}")
        return None

def watchdog_loop():
    """Monitors the gateway health and restarts it if it fails."""
    global gateway_process
    print("🛡️ Self-Healing Watchdog active.")
    
    while True:
        time.sleep(60) # Check every minute
        
        # 1. Check if process is still running
        if gateway_process and gateway_process.poll() is not None:
            print("⚠️ Gateway process exited. Restarting...")
            start_openclaw_gateway()
            continue
            
        # 2. Check if API is responsive
        try:
            is_healthy = asyncio.run(check_gateway_health(timeout=5))
            if not is_healthy:
                print("⚠️ Gateway unresponsive. Force restarting...")
                if gateway_process:
                    gateway_process.terminate()
                    gateway_process.wait()
                start_openclaw_gateway()
        except Exception:
            pass

def main():
    start_openclaw_gateway()
    
    # Start the Watchdog in a background thread
    watchdog_thread = threading.Thread(target=watchdog_loop, daemon=True)
    watchdog_thread.start()
    
    # Start the Strategic Scheduler
    start_scheduler()
    
    # Start the Heartbeat Monitor (Autonomous Tasks)
    hb_interval = int(os.getenv("HEARTBEAT_INTERVAL", "15"))
    hb_thread = threading.Thread(target=heartbeat_loop, args=(hb_interval,), daemon=True)
    hb_thread.start()
    
    platform = os.getenv("PLATFORM", "cli").lower()

    try:
        if "--telegram" in sys.argv or platform == "telegram":
            print("🤖 Starting Telegram platform...")
            print("💡 Reminder: Find your bot in Telegram and send /start to begin.")
            from brain.platforms.telegram_bot import run_telegram
            run_telegram()
        elif "--cli" in sys.argv or platform == "cli":
            from brain.platforms.cli import run_cli
            run_cli()
        else:
            print("FriendlyClaw")
            print("Usage: python main.py --telegram | --cli")
    finally:
        if gateway_process:
            print("🛑 Shutting down OpenClaw Gateway...")
            gateway_process.terminate()

if __name__ == "__main__":
    main()
