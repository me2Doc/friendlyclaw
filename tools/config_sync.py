import os
import json
import logging
from pathlib import Path

logger = logging.getLogger("FriendlyClaw.ConfigSync")

def sync_openclaw_config():
    """
    Synchronizes settings from FriendlyClaw .env to the internal OpenClaw system_body.
    Ensures the unified system has a single source of truth.
    """
    # Paths
    oc_config_path = Path("system_body/openclaw.json")
    
    # If the config doesn't exist, we create a base one
    if not oc_config_path.exists():
        logger.info("Initializing system_body/openclaw.json...")
        base_config = {
            "gateway": {"port": 18789, "mode": "local", "bind": "loopback"},
            "channels": {"telegram": {"enabled": False}, "whatsapp": {"enabled": False}},
            "agents": {"defaults": {"workspace": os.path.abspath("data/workspace")}}
        }
        oc_config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(oc_config_path, "w") as f:
            json.dump(base_config, f, indent=2)

    try:
        with open(oc_config_path, "r") as f:
            config = json.load(f)

        # Sync Gateway Port from ENV if present
        env_port = os.getenv("OPENCLAW_PORT")
        if env_port:
            config["gateway"]["port"] = int(env_port)
            logger.info(f"Synced Gateway Port: {env_port}")

        # Sync Telegram if FriendlyClaw is in Telegram mode
        if os.getenv("PLATFORM") == "telegram":
            # We disable OpenClaw's native telegram to avoid double-bots, 
            # but we keep the config ready if needed.
            config["channels"]["telegram"]["enabled"] = False
            
        # Write back the synced config
        with open(oc_config_path, "w") as f:
            json.dump(config, f, indent=2)
            
        return True
    except Exception as e:
        logger.error(f"Config sync failed: {e}")
        return False
