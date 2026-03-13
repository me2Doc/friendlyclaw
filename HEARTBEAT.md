# 💓 FriendlyClaw Heartbeat Missions

This file contains the high-level objectives that FriendlyClaw will autonomously check every 15 minutes.
You can edit this file at any time to change the agent's background focus.

## 🎯 Current Missions

1. **System Health:** Check disk space and memory usage. Alert if disk > 90%.
2. **Visual Sentinel:** Run a `visual_pulse` to check the environment or screen state.
3. **Task Monitoring:** Check for any "todo" files in the workspace and suggest progress.

---
*Note: FriendlyClaw will read this file during its Heartbeat cycle. It may also self-update this file to report mission progress.*
