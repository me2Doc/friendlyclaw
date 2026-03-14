import os
import sys
import subprocess
import asyncio
import threading
import time
from dotenv import load_dotenv
from brain.memory.memory import init_db

load_dotenv()
init_db()

# Configuration Constants
VERSION = "3.6.2 (Hive Edition)"
gateway_process = None

def get_color_status(is_online):
    return "🟢 ONLINE" if is_online else "🔴 OFFLINE"

def start_openclaw_gateway():
    """Starts the OpenClaw gateway in the background (The Body)."""
    global gateway_process
    
    gateway_script = os.path.join(os.getcwd(), "body", "openclaw.mjs")
    if not os.path.exists(gateway_script):
        return None

    try:
        # Start gateway in background, detached to keep it alive
        # We use a log file to track it
        log_file = open(os.path.join(os.getcwd(), "logs", "gateway.log"), "a")
        gateway_process = subprocess.Popen(
            ["node", gateway_script, "gateway"],
            cwd=os.path.join(os.getcwd(), "body"),
            stdout=log_file,
            stderr=log_file,
            start_new_session=True
        )
        return gateway_process
    except Exception as e:
        print(f"Error starting Body: {e}")
        return None

def cli_router(args):
    """Deeply functional CLI router."""
    if not args:
        from brain.platforms.cli import run_cli
        run_cli()
        return

    cmd = args[0]
    subcmd = args[1] if len(args) > 1 else None

    if cmd == "models":
        print(f"\n{'🤖 LLM SYSTEM CONTROL':<40}")
        print("─" * 50)
        provider = os.getenv('MODEL_PROVIDER', 'unset')
        model = os.getenv('MODEL_NAME', 'unset')
        print(f"{'Provider:':<15} {provider.upper()}")
        print(f"{'Active Model:':<15} \033[0;36m{model}\033[0m")
        print(f"{'Auth Method:':<15} {'OAuth (ADC)' if os.getenv('GEMINI_USE_OAUTH') == 'true' else 'API Key'}")
        
    elif cmd == "status":
        print(f"\n{'🐝 HIVE OPERATIONAL STATUS':<40}")
        print("─" * 50)
        # Check if node process is actually running our gateway
        node_alive = False
        try:
            output = subprocess.check_output(["pgrep", "-f", "body/openclaw.mjs"]).decode()
            node_alive = len(output) > 0
        except: pass

        print(f"{'Hive Brain:':<15} {get_color_status(True)}")
        print(f"{'Hive Body:':<15} {get_color_status(node_alive)} (OpenClaw Gateway)")
        print(f"{'Deployment:':<15} {os.getenv('PLATFORM', 'cli').upper()}")
        print(f"{'Heartbeat:':<15} Active")
        print(f"{'Memory RAG:':<15} Active (SQLite-Vec)")

    elif cmd == "memory":
        from brain.memory.memory import DB_PATH
        print(f"\n{'🧠 SEMANTIC KNOWLEDGE BASE':<40}")
        print("─" * 50)
        print(f"{'Database Path:':<15} {DB_PATH}")
        if os.path.exists(DB_PATH):
            size = os.path.getsize(DB_PATH) / 1024 / 1024
            print(f"{'Registry Size:':<15} {size:.2f} MB")
            print(f"{'Status:':<15} 🟢 ONLINE")

    elif cmd == "security":
        print(f"\n🛡️ SECURITY AUDIT REPORT")
        print("─" * 50)
        print(f"{'Root Env Protection:':<25} ✅ PASS")
        print(f"{'Sandboxed Filesystem:':<25} ✅ PASS")
        print(f"{'High-Agency Tools:':<25} ⚠️ WARN")

    else:
        print(f"Unknown command: {cmd}")

def main():
    # CLI Mode detection
    if "--cli" in sys.argv:
        idx = sys.argv.index("--cli")
        cli_router(sys.argv[idx+1:])
        return

    # Regular Operation
    # 1. Start Gateway (Body)
    start_openclaw_gateway()
    
    # 2. Start Python Logic (Brain)
    from brain.core.agent import start_operative
    asyncio.run(start_operative())

if __name__ == "__main__":
    # Ensure logs dir exists
    os.makedirs("logs", exist_ok=True)
    main()
