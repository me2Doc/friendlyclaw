import os
import sys
from dotenv import load_dotenv
from memory.memory import init_db

load_dotenv()
init_db()

def main():
    platform = os.getenv("PLATFORM", "cli").lower()

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

if __name__ == "__main__":
    main()
