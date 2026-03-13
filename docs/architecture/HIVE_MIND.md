# 🧠 The Hive Mind Architecture

FriendlyClaw Hive is a multi-threaded autonomous system that splits strategic reasoning from technical execution.

## 🏗️ Core Layers

### 1. The Commander (Main Brain)
Located in `core/agent.py`. This is the primary LLM interface. It handles real-time chat, tool selection, and overall mission strategy. It uses **Recursive Chain-of-Thought** to solve complex problems in a single turn.

### 2. The Swarm (Ghost Workers)
Located in `core/swarm.py`. The Commander can delegate long-running or parallel tasks to this layer.
- **Workers:** Independent threads that run their own AI turns.
- **Isolation:** Each worker has its own objective and context, preventing "noise" in the main chat.
- **Persistence:** Tasks are tracked in the SQLite `tasks` table.

### 3. The Eternal Memory (Semantic Layer)
Located in `memory/memory.py`. 
- **RAG:** Every interaction is embedded using `sqlite-vec`.
- **Retrieval:** The AI performs a semantic search on every turn to pull in relevant history from months or years ago.

### 4. The Body (Execution Gateway)
Located in `system_body/`. Powered by **OpenClaw**, this Node.js layer provides the "muscles" (Shell, UI control, Media, etc.).

---

## 🔗 Data Flow
1. **Input:** User sends message via Telegram/CLI.
2. **Context:** Brain retrieves facts/memories from SQLite.
3. **Reasoning:** Commander decides if a tool is needed.
4. **Delegation:** If the task is heavy, Brain spawns a **Swarm Worker**.
5. **Execution:** Body executes system commands.
6. **Synthesis:** Commander merges worker findings and replies to user.
