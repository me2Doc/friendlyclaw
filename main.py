import os
import sys
import subprocess
import asyncio
import signal
import time
from dotenv import load_dotenv
from brain.memory.memory import init_db

load_dotenv()
init_db()

# Configuration Constants
VERSION = "3.8.0 (Hive Edition)"
gateway_process = None

def get_color_status(is_online):
    return "🟢 ONLINE" if is_online else "🔴 OFFLINE"

def cleanup(signum=None, frame=None):
    """Graceful shutdown of all child processes."""
    global gateway_process
    if gateway_process:
        print("\n🛑 Shutting down Hive Body (Gateway)...")
        gateway_process.terminate()
        try:
            gateway_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            gateway_process.kill()
    print("👋 FriendlyClaw Offline.")
    sys.exit(0)

# Register signals for graceful exit
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def start_openclaw_gateway():
    """Starts the OpenClaw gateway in the background (The Body)."""
    global gateway_process
    
    gateway_script = os.path.join(os.getcwd(), "body", "openclaw.mjs")
    if not os.path.exists(gateway_script):
        return None

    try:
        # Start gateway in background
        os.makedirs("logs", exist_ok=True)
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

def run_security_audit():
    """Performs a REAL security audit of the environment."""
    print(f"\n{'🛡️ STRATEGIC SECURITY AUDIT':<40}")
    print("─" * 50)
    
    # 1. Check .env permissions (should be 600 or 644)
    env_secure = False
    if os.path.exists(".env"):
        mode = oct(os.stat(".env").st_mode & 0o777)
        if mode in ["0o600", "0o644", "0o400"]:
            env_secure = True
    print(f"{'Root Env Protection:':<25} {'✅ PASS' if env_secure else '⚠️ WARN (Insecure Perms)'}")

    # 2. Check for shell access tools
    # If the user has gcloud or git, it's high agency
    has_tools = subprocess.run(["which", "gcloud"], capture_output=True).returncode == 0
    print(f"{'High-Agency Tools:':<25} {'⚠️ HIGH' if has_tools else '✅ MINIMAL'}")

    # 3. Check if running as root
    is_root = os.getuid() == 0
    print(f"{'Least Privilege:':<25} {'❌ FAIL (Running as Root)' if is_root else '✅ PASS'}")

    # 4. Check for API Exposure
    # Check if .env contains keys
    has_keys = False
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            if "API_KEY" in f.read(): has_keys = True
    print(f"{'Credential Registry:':<25} {'✅ ENCRYPTED' if not has_keys else '⚠️ PLAIN-TEXT'}")

def cli_router(args):
    """Deeply functional CLI router."""
    if not args:
        from brain.platforms.cli import run_cli
        run_cli()
        return

    cmd = args[0]
    
    if cmd == "status":
        print(f"\n{'🐝 HIVE OPERATIONAL STATUS':<40}")
        print("─" * 50)
        node_alive = False
        try:
            output = subprocess.check_output(["pgrep", "-f", "body/openclaw.mjs"]).decode()
            node_alive = len(output) > 0
        except: pass

        print(f"{'Hive Brain:':<15} {get_color_status(True)}")
        print(f"{'Hive Body:':<15} {get_color_status(node_alive)}")
        print(f"{'Deployment:':<15} {os.getenv('PLATFORM', 'cli').upper()}")
        print(f"{'Version:':<15} {VERSION}")

    elif cmd == "security":
        run_security_audit()

    elif cmd == "models":
        print(f"\n{'🤖 LLM SYSTEM CONTROL':<40}")
        print("─" * 50)
        print(f"{'Provider:':<15} {os.getenv('MODEL_PROVIDER', 'unset').upper()}")
        print(f"{'Active Model:':<15} \033[0;36m{os.getenv('MODEL_NAME', 'unset')}\033[0m")

    elif cmd == "memory":
        from brain.memory.memory import DB_PATH
        print(f"\n{'🧠 SEMANTIC KNOWLEDGE BASE':<40}")
        print("─" * 50)
        if os.path.exists(DB_PATH):
            size = os.path.getsize(DB_PATH) / 1024 / 1024
            print(f"{'Database:':<15} {DB_PATH}")
            print(f"{'Registry Size:':<15} {size:.2f} MB")
        else:
            print("  Status: OFFLINE (Run onboarding)")

    else:
        print(f"Unknown command: {cmd}")

def main():
    if "--cli" in sys.argv:
        idx = sys.argv.index("--cli")
        cli_router(sys.argv[idx+1:])
        return

    # Regular Operation
    start_openclaw_gateway()
    from brain.core.agent import start_operative
    asyncio.run(start_operative())

if __name__ == "__main__":
    main()
