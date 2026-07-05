# VanillaForge Agent

VanillaForge is a high-precision financial analysis agent built on Google's **Agent Development Kit (ADK) 2.0**. Originally a generic options derivative conversational assistant, it has been heavily customized following the advanced "Agent Skills" from Google ADK architecture, specifically leveraging **Progressive Disclosure** and **Shift Intelligence Left** to minimize token usage, resolve issues before execution, and remain highly efficient and secure.

## Architecture Overview

The agent is designed as a single, deterministic orchestration engine (`VanillaForge_agent`) locked at `temperature=0.1`. Instead of a complex, brittle routing graph, the agent dynamically discovers and loads independent tools from the `skills/` directory at runtime only when needed, in order to save token usage and avoid context memory rot (hallucination).

```text
                  [START]
                     │
              [VanillaForge_agent]
             /       │       \      \
 (Calls Agent Skill) │        \      \ 
           /         │         \      \
          ▼          ▼          ▼      ▼
   [pricing_skill] [data_skill] [documentation_skill] ...
          │          │          │      │
          ▼          ▼          ▼      ▼
    [      skill_loader.py (SkillToolset)       ]
    [ Injects __agent_instructions__ from YAML  ]
          │          │          │      │
           \         │         /      /
            \        │        /      /
             ▼       ▼       ▼      ▼
              [VanillaForge_agent]
                     │
               (User Resumes)
```

### The `SkillToolset` Loader (`app/skill_loader.py`)
At the core of the architecture is the automated `skill_loader.py`. 
When the agent starts, it scans the `skills/` directory and parses the lightweight YAML metadata from each `SKILL.md` file. It then automatically intercepts tool execution to inject the heavy Markdown instructions (`__agent_instructions__`) into the payload *only when the skill is actually used*. This prevents "Context Rot" and keeps the agent fast and cheap.

## Available Skills

The `VanillaForge_agent` currently possesses 5 core capabilities:

1. **`documentation_skill`**: **Reads options textbooks to teach you financial theory.** It performs RAG over a local ChromaDB to answer complex educational options theory questions without hallucinating. Includes also a built-in ingestion tool (`scripts/ingest_pdfs.py`) to easily drop new PDFs into `Documents_options/` and instantly expand the agent's knowledge base.
2. **`company_information_skill`**: **Fetches basic company profiles and financials.** It scrapes and retrieves specific fundamental metadata about a publicly traded company.
3. **`pricing_skill`**: **Calculates the fair price and risk metrics of any strategy based on European vanilla options.** It acts as a Black-Scholes-Merton (BSM) calculator for European options. If the user omits inputs, an internal sub-agent seamlessly fetches the live Spot Price, Implied Volatility, and Dividend Yield from Google Search before computing the option premium and Greeks.
4. **`data_skill`**: **Downloads historical market data and draws pricing charts.** It uses `yfinance` to download market data, persists massive datasets locally as high-performance `.parquet` and `.csv` files, and generates `seaborn` visualizations.
5. **`news_sentiment_skill`**: **Reads the news to tell you if the market is bullish or bearish on a stock.** It retrieves the top 10 most recent news articles for an equity and performs a rigid semantic sentiment analysis on each, returning a structured 0-100 score and thematic breakdown.

---

## Directory Structure

*   **`app/agent.py`**: The central orchestrator Agent configuration and persona.
*   **`app/skill_loader.py`**: The automated Progressive Disclosure framework loader.
*   **`skills/`**: Contains the decoupled skill logic. Every skill has its own `SKILL.md` (metadata and instructions) and a `scripts/` folder containing the Python tools.
*   **`scripts/ingest_pdfs.py`**: Pipeline script to extract, chunk, and embed new PDFs into the local ChromaDB database.
*   **`Documents_options/`**: Drop folder for new PDF textbooks and references.
*   **`evals/eval_cases.json`**: The test suite used for Evaluation-Driven Development (EDD) of all skills.
*   **`tests/`**: Pytest assertions covering the agent flow and skill capabilities.

---

## Getting Started

### 1. Prerequisites
Ensure you have `uv` installed. If not, follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Install `google-agents-cli`:
```powershell
uv tool install google-agents-cli
```

### 2. Configure Local Authentication
Duplicate the `.env_example` template:
```powershell
copy .env_example .env
```

Set your `GEMINI_API_KEY` in the `.env` file to authenticate with Google AI Studio.

### 3. Install Dependencies
Run the install command to sync package dependencies:
```powershell
agents-cli install
```

---

## Running the Agent

### Command Line Smoke Tests
Run a quick educational test query:
```powershell
agents-cli run "What is a call option?"
```

Test the advanced CVX pricing calculation (with automated dividend yield retrieval):
```powershell
agents-cli run "Price a 1-year call option on CVX with a strike of 150."
```

### Interactive Web Playground
Launch the local web-based playground to chat with the agent. 

On Windows (or within PowerShell), run the playground using the direct runner:
```powershell
uv run adk web . --host 127.0.0.1 --port 8080 --reload_agents
```

On Linux/macOS, you can use the standard CLI runner:
```bash
agents-cli playground
```

Once started, open your browser and navigate to:
[http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)
