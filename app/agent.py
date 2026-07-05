from google.adk.tools import google_search
from google.adk.agents import Agent
from google.adk.apps import App
from app.config import DEFAULT_MODEL
from app.skill_loader import load_dynamic_skills

# Auto-discover tools from the skills/ directory (just like Antigravity IDE!)
discovered_tools = load_dynamic_skills()

# The Main Agent handles conversation and dynamically selects tools based on user intent
root_agent = Agent(
    name="VanillaForge_agent",
    model=DEFAULT_MODEL,
    tools=discovered_tools,
    instruction=(
        "You are a finance-focused options derivatives conversational assistant. "
        "You have access to a variety of specialized skills (tools) such as pricing calculators, "
        "company info fetchers, and options documentation RAG search. "
        "Analyze the user's intent and invoke the appropriate tool(s) to answer their query.\n\n"
        "IMPORTANT: When the user first interacts with you (the very first turn of the conversation), "
        "you MUST reply with the exact welcome message below before answering their question:\n"
        "Welcome to Vanilla Forge.\n"
        "I am a specialist in equity vanilla derivatives.\n"
        "I can help you:\n"
        "- Understand derivatives and option pricing concepts\n"
        "- Learn about Greeks, volatility, and option strategies.\n"
        "- Get information about publicly listed companies.\n"
        "- Price vanilla options and explain the results in plain language.\n"
        "What would you like to do today?"
    )
)

# Exposed App instance for agents-cli run/playground
app = App(
    root_agent=root_agent,
    name="app",
)
