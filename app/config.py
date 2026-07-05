import os
from dotenv import load_dotenv

# Resolve absolute path to project root (parent of app/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, ".env")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# ==============================================================================
# CENTRAL CONFIGURATION FOR VANILLAFORGE AGENT
# ==============================================================================

# Default model configuration as requested
DEFAULT_MODEL = "gemini-3.1-flash-lite"

# Path to the skills directory (located at the root level of the project)
SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills"
)


def load_skill_instructions(skill_name: str) -> str:
    """
    Dynamically loads the SKILL.md file for a given skill to act as the
    system instructions for model invocations.
    """
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        raise FileNotFoundError(
            f"SKILL.md for skill '{skill_name}' not found at {skill_path}"
        )

    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()
