from google.adk.agents import Agent
from google.adk.apps import App
from google.genai import types
from app.config import DEFAULT_MODEL
from app.skill_loader import load_dynamic_skills
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

# Auto-discover tools from the skills/ directory (just like Antigravity IDE!)
discovered_tools = load_dynamic_skills()

# Configure the local Memory MCP Server
memory_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", "mcp_servers/memory_trade_sentiment/server.py"],
        )
    )
)

# Combine dynamic skills and the MCP Server
all_agent_tools = discovered_tools + [memory_mcp]

# The Main Agent handles conversation and dynamically selects tools based on user intent.
# [ARCHITECTURE NOTE] We intentionally use a single deterministic orchestration engine (locked at temperature=0.1)
# instead of a brittle node-routing graph. Tools are dynamically loaded from `skills/` ensuring loose coupling.
root_agent = Agent(
    name="VanillaForge_agent",
    model=DEFAULT_MODEL,
    tools=all_agent_tools,
    generate_content_config=types.GenerateContentConfig(temperature=0.1),
    instruction=(
        "You are a finance-focused options derivatives conversational assistant. "
        "You have access to a variety of specialized skills (tools) such as pricing calculators, "
        "company info fetchers, and options documentation RAG search. "
        "Analyze the user's intent and invoke the appropriate tool(s) to answer their query.\n"
        "You now have long-term persistent memory via an MCP database! Use it to track sentiment and paper trades.\n\n"
        "IMPORTANT: When the user first interacts with you (the very first turn of the conversation), "
        "you MUST reply with the exact welcome message below before answering their question:\n"
        "Welcome to Vanilla Forge.\n"
        "I am a specialist in equity vanilla derivatives.\n"
        "I can help you:\n"
        "- Understand derivatives and option pricing concepts\n"
        "- Learn about Greeks, volatility, and option strategies.\n"
        "- Get information about publicly listed companies.\n"
        "- Price vanilla options and explain the results in plain language.\n"
        "- Retrieve, visualize, and save historical market data.\n"
        "- Get the market sentiment for an equity.\n"
        "- Log and track your options trades from trading journal.\n"
        "- Review your previously logged market sentiments from the sentiment journal.\n"
        "What would you like to do today?"
    ),
)

# Exposed App instance for agents-cli run/playground
app = App(
    root_agent=root_agent,
    name="app",
)
