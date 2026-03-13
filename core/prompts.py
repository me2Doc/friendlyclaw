# Specialized Prompt Directives for FriendlyClaw Hive

HEARTBEAT_SENTINEL_PROMPT = """[HEARTBEAT MISSION] 
Here are my current background objectives:

{missions}

Perform a quick audit of these objectives. Use tools if necessary. 
If everything is normal, do not notify the user. 
If an anomaly is detected, provide a brief alert."""

SWARM_SUBAGENT_PROMPT = """[SWARM SUB-AGENT OBJECTIVE] 
{objective}

Perform this mission autonomously. Use tools as needed. 
Your results will be synthesized by the primary partner. 
Provide a comprehensive final report of your findings."""

MODE_DIRECTIVE_SENTINEL = "\n🚨 AUTONOMOUS SENTINEL MODE ACTIVE: You are running a background heartbeat check. Be concise. Only alert if something is wrong or a mission objective is met."
