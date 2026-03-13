import os
import sys
import subprocess
import asyncio
from dotenv import load_dotenv
from memory.memory import init_db
from tools.openclaw_bridge import check_gateway_health

load_dotenv()
init_db()

def start_openclaw_gateway():
    """Starts the OpenClaw gateway in the background if it's not already running."""
    gateway_script = os.path.join(os.getcwd(), "system_body", "openclaw.mjs")
    if not os.path.exists(gateway_script):
        print("Warning: OpenClaw gateway script (system_body/openclaw.mjs) not found. System tools may be unavailable.")
        return None

    print("🚀 Starting OpenClaw Gateway (System Body)...")
    try:
        # Start gateway in background
        process = subprocess.Popen(
            ["node", gateway_script, "gateway"],
            cwd=os.path.join(os.getcwd(), "system_body"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for the gateway to become healthy instead of a magic sleep
        is_up = asyncio.run(check_gateway_health(timeout=30))
        if not is_up:
            print("⚠️ Warning: Gateway did not become healthy in time. Some system actions might fail.")
            
        return process
    except Exception as e:
        print(f"Error starting OpenClaw gateway: {e}")
        return None

def main():
    gateway_process = start_openclaw_gateway()
    
    platform = os.getenv("PLATFORM", "cli").lower()

    try:
        if "--telegram" in sys.argv or platform == "telegram":
            from platforms.telegram_bot import run_telegram
            run_telegram()
        elif "--cli" in sys.argv or platform == "cli":
            from platforms.cli import run_cli
            run_cli()
        else:
            print("FriendlyClaw")
            print("Usage: python main.py --telegram | --cli")
            print("Or set PLATFORM=telegram|cli in .env")
    finally:
        if gateway_process:
            print("🛑 Shutting down OpenClaw Gateway...")
            gateway_process.terminate()

if __name__ == "__main__":
    main()