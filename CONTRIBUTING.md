# Contributing to FriendlyClaw 🦀

First off, thank you for considering contributing to FriendlyClaw! It’s people like you who make this a powerful tool for everyone.

## 🧠 Our Philosophy
FriendlyClaw is a **High-Agency AI Operator**. We prioritize:
- **Resilience:** The Brain and Body must stay synced.
- **Privacy:** User data and memories stay local.
- **Agency:** The AI should be able to execute complex system tasks reliably.

## 🛠️ How to Contribute

### 1. Reporting Bugs
- Check the [Issues](https://github.com/me2Doc/friendlyclaw/issues) to see if the bug has already been reported.
- If not, open a new issue. Include your OS, Python/Node versions, and steps to reproduce the error.

### 2. Suggesting Features
- We love new ideas! Open an issue with the tag `enhancement` and describe how the feature would improve the "Brain" (Logic) or "Body" (Execution).

### 3. Making Changes
1. **Fork the Repo:** Create your own copy of the project.
2. **Create a Branch:** Work on a specific feature (e.g., `git checkout -b feat/new-skill`).
3. **Commit Your Changes:** Use clear, descriptive commit messages (e.g., `git commit -m "Added Spotify playback skill to body"`).
4. **Push & PR:** Push to your fork and submit a **Pull Request (PR)** to our `main` branch.

## 📂 Coding Standards
- **The Brain:** Written in **Python 3**. Core logic resides in `brain/`.
- **The Body:** Powered by **OpenClaw (Node.js)**. Source code in `body/`.
- **Security:** Never commit secrets or API keys. Ensure all new system commands pass through the security intercepts in `brain/core/agent.py`.

## 🦾 Skill Development
- **Native Skills:** Add to `body/skills/` using the OpenClaw Markdown format.
- **Logic Skills:** Add to `brain/skills/custom/` using the FriendlyClaw JSON format.

---
*By contributing, you agree that your contributions will be licensed under the project's MIT License.*
