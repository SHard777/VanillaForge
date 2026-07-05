from google.genai import Client
from google.genai import types
import os


def get_company_profile(company_name: str) -> str:
    """
    Retrieves the corporate profile and business sector context for a listed company.
    """
    client = Client()

    # Read the SKILL.md body to use as system instructions
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skill_md_path = os.path.join(os.path.dirname(current_dir), "SKILL.md")

    system_instruction = ""
    if os.path.exists(skill_md_path):
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Skip the YAML frontmatter
            if content.startswith("---"):
                end_idx = content.find("---", 3)
                if end_idx != -1:
                    system_instruction = content[end_idx + 3 :].strip()
            else:
                system_instruction = content.strip()

    prompt = (
        f"Retrieve the corporate profile, market context, and financial information for the following company: {company_name}\n\n"
        f"CRITICAL INSTRUCTION: You MUST strictly format your response using the exact 6-point 'Response Structure' "
        f"defined in your system instructions. Do NOT deviate from this structure."
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    return response.text
