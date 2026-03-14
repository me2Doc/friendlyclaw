import os
from pathlib import Path

CONFIG_QUESTIONS = [
    {
        "key": "MODEL_PROVIDER",
        "text": "Select Model Provider (gemini / openai / openrouter / custom):",
        "options": ["gemini", "openai", "openrouter", "custom"]
    },
    {
        "key": "MODEL_NAME",
        "text": "Enter Model Name (e.g., gemini-2.0-flash, gpt-4o, etc.):",
    },
    {
        "key": "GEMINI_API_KEY",
        "text": "Enter Gemini API Key (or skip):",
        "condition": lambda updates: updates.get("MODEL_PROVIDER") == "gemini"
    },
    {
        "key": "OPENAI_API_KEY",
        "text": "Enter OpenAI API Key (or skip):",
        "condition": lambda updates: updates.get("MODEL_PROVIDER") == "openai"
    },
    {
        "key": "OPENROUTER_API_KEY",
        "text": "Enter OpenRouter API Key (or skip):",
        "condition": lambda updates: updates.get("MODEL_PROVIDER") == "openrouter"
    },
    {
        "key": "CUSTOM_BASE_URL",
        "text": "Enter Custom Base URL (e.g., http://localhost:11434/v1):",
        "condition": lambda updates: updates.get("MODEL_PROVIDER") == "custom"
    },
    {
        "key": "CUSTOM_API_KEY",
        "text": "Enter Custom API Key (or 'fake'):",
        "condition": lambda updates: updates.get("MODEL_PROVIDER") == "custom"
    }
]

class ConfigSession:
    def __init__(self):
        self.step = 0
        self.updates = {}
        self.active = False

    def start(self):
        self.step = 0
        self.updates = {}
        self.active = True
        return CONFIG_QUESTIONS[0]["text"]

    def process_answer(self, answer: str):
        if not self.active:
            return None

        current_q = CONFIG_QUESTIONS[self.step]
        key = current_q["key"]
        
        if answer.strip().lower() == "skip":
            feedback = f"Skipped {key}. Keeping current value."
        else:
            self.updates[key] = answer.strip()
            feedback = f"Set {key} to {answer.strip()}."

        # Move to next applicable question
        self.step += 1
        while self.step < len(CONFIG_QUESTIONS):
            next_q = CONFIG_QUESTIONS[self.step]
            condition = next_q.get("condition")
            if not condition or condition(self.updates):
                return {"done": False, "text": f"{feedback}\n\n{next_q['text']}"}
            self.step += 1

        self.active = False
        self.save_to_env()
        return {"done": True, "text": f"{feedback}\n\nConfiguration updated successfully."}

    def save_to_env(self):
        env_path = Path(".env")
        if not env_path.exists():
            return

        with open(env_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        updated_keys = set()

        for line in lines:
            if "=" in line and not line.strip().startswith("#"):
                key = line.split("=")[0].strip()
                if key in self.updates:
                    new_lines.append(f"{key}={self.updates[key]}\n")
                    updated_keys.add(key)
                    # Update current environment
                    os.environ[key] = self.updates[key]
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Add missing keys if any
        for key, value in self.updates.items():
            if key not in updated_keys:
                new_lines.append(f"{key}={value}\n")
                os.environ[key] = value

        with open(env_path, "w") as f:
            f.writelines(new_lines)

# Global session tracker for CLI
cli_config_session = ConfigSession()
