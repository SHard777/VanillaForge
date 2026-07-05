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
        f"defined in your system instructions. Do NOT deviate from this structure.\n\n"
        f"CRITICAL INSTRUCTION 2: You MUST use the Google Search tool to aggressively find the LIVE financial metrics for this company. Specifically, you must locate the current 'Market Cap', 'P/E Ratio', 'Beta', 'Dividend Yield', and '52 Week High/Low'. Do NOT output N/A unless absolutely impossible to find.\n\n"
        f"CRITICAL INSTRUCTION 3: You MUST append the following JSON block at the very end of your response, wrapped in a ```json markdown block.\n"
        f"Fill in the actual values based on your research.\n"
        f"```json\n"
        f"{{\n"
        f'  "ui_action": "UPDATE_COMPANY_INFO",\n'
        f'  "data": {{\n'
        f'    "ticker": "TICKER_SYMBOL",\n'
        f'    "name": "COMPANY_NAME",\n'
        f'    "sector": "SECTOR",\n'
        f'    "industry": "INDUSTRY",\n'
        f'    "marketCap": "MARKET_CAP",\n'
        f'    "peRatio": "PE_RATIO",\n'
        f'    "beta": "BETA",\n'
        f'    "dividendYield": "DIV_YIELD",\n'
        f'    "fiftyTwoWeekHigh": "52W_HIGH",\n'
        f'    "fiftyTwoWeekLow": "52W_LOW",\n'
        f'    "description": "1 paragraph description",\n'
        f'    "businessSegments": "Details about the business segments",\n'
        f'    "competitivePosition": "Details about competitive position and industry context",\n'
        f'    "keyFinancialMetrics": "Details about key financial metrics",\n'
        f'    "keyValuationMetrics": "Details about key valuation metrics",\n'
        f'    "investorTakeaways": "Key takeaways for an investor"\n'
        f"  }}\n"
        f"}}\n"
        f"```"
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    text = response.text
    import re
    import json
    import requests

    # Extreme Robust JSON extraction: Find the last major JSON block at the end of the text
    idx = text.rfind("\n{")
    if idx == -1:
        idx = text.rfind("```{")
        if idx != -1:
            idx += 3

    if idx != -1:
        json_str = text[idx:].strip()
        end_idx = json_str.rfind("}")
        if end_idx != -1:
            json_str = json_str[: end_idx + 1]

            # Remove JSON from the final text sent to user (do this BEFORE the try-except)
            text_to_strip = text[idx:].strip()
            text = text.replace(text_to_strip, "").strip()
            text = re.sub(r"```json\s*$", "", text).strip()
            text = re.sub(r"```a2ui\s*$", "", text).strip()

            try:
                payload = json.loads(json_str)

                # Normalize hallucinated keys
                if "ui_action" not in payload:
                    payload["ui_action"] = "UPDATE_COMPANY_INFO"
                if "data" not in payload:
                    payload = {"ui_action": "UPDATE_COMPANY_INFO", "data": payload}

                requests.post(
                    "http://localhost:8000/api/internal/a2ui", json=payload, timeout=0.5
                )
            except Exception:
                pass
    return {"status": "success", "profile_text": text}
