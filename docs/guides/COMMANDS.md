# 🕹️ Command Reference

FriendlyClaw presents a unified interface across all platforms. Commands can be typed directly or triggered via native buttons in Telegram.

## 🛠️ Platform Commands
- `/start`: Initialize profile and begin onboarding.
- `/help`: Display dynamic help text based on active skills.
- `/memory`: Show everything the AI remembers about you (Facts/Notes).
- `/tasks`: View the **Strategic Task Board** (status of background workers).
- `/synthesize [task_id]`: Pull the final report from a background mission.
- `/model [name]`: Switch the active LLM model for the current session.
- `/forget`: Wipe all personal data and memory (Requires confirmation).

## 🚀 Strategic Tools (AI-Native)
The AI uses these tools autonomously during conversation:

| Tool | Purpose | Example |
| :--- | :--- | :--- |
| `spawn_subagent` | Delegate work to the background swarm. | "Spawn a sub-agent to research RISC-V." |
| `visual_pulse` | Perform a visual audit (Camera/Screen). | "Run a visual pulse every 15 mins." |
| `run_shell` | Execute system commands (Human-in-the-loop). | "Update my system packages." |
| `deep_read_url` | High-fidelity web page extraction. | "Read this technical documentation." |
| `remember_info` | Commit data to Eternal Memory (RAG). | "Remember that I use Arch Linux." |

## 💓 Heartbeat Missions
Edit the `HEARTBEAT.md` file in the root directory to set background missions.
- The AI reads this file every 15 minutes.
- Example mission: "Check for security updates and notify me if critical."
