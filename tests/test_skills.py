import sys
import os
import json
from pathlib import Path

# Add the project root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.skills import get_all_skills, get_skill_prompt

def test_core_skills_loading():
    skills = get_all_skills()
    triggers = [s['trigger'] for s in skills.values()]
    if "/analyze" in triggers:
        print("✅ Core skills loading test passed")
    else:
        raise ValueError("Core skill /analyze not found")

def test_custom_skill_loading():
    # Create a temporary custom skill
    custom_dir = Path("brain/skills/custom")
    custom_dir.mkdir(exist_ok=True)
    test_skill_path = custom_dir / "test_joke.json"
    
    test_data = {
        "trigger": "/joke",
        "description": "Tell a funny joke",
        "prompt": "Tell a joke that is actually funny."
    }
    
    with open(test_skill_path, "w") as f:
        json.dump(test_data, f)
    
    try:
        skills = get_all_skills()
        triggers = [s['trigger'] for s in skills.values()]
        if "/joke" in triggers:
            prompt = get_skill_prompt("/joke")
            if prompt == test_data["prompt"]:
                print("✅ Custom skill loading test passed")
            else:
                raise ValueError(f"Prompt mismatch: expected {test_data['prompt']}, got {prompt}")
        else:
            raise ValueError("Custom skill /joke not found")
    finally:
        # Cleanup
        if test_skill_path.exists():
            test_skill_path.unlink()

if __name__ == "__main__":
    try:
        test_core_skills_loading()
        test_custom_skill_loading()
        print("\nAll skill tests passed! 🚀")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
