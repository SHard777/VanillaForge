# VanillaForge Agent

VanillaForge is a finance-focused conversational options derivatives agent built using the **ADK 2.0 Workflow Graph API**. It handles options derivative education, company information, and options pricing using the standard Black-Scholes-Merton model and analytical Greeks computations.

## Architecture

The agent is designed as a **single agent** utilizing a cyclic routing graph to manage multi-turn conversations:

```
                  [START]
                     │
              [router_node]
              /    │     \   \
  "documentation"  │      \   "general" (fallback)
        /    "company_info" \       \
       ▼           ▼         ▼       ▼
 [doc_node]   [info_node] [pricing_node] [gen_node]
       \           │         /       /
        ▼          ▼        ▼       ▼
              [responder_node] <─── Yields RequestInput (HITL)
                     │
              (User Resumes)
                     │
                     ▼
              (Loops to Router)
```

### Components
*   **`config.py`**: Central model config (`gemini-3.1-flash-lite`) and SKILL.md loading utility.
*   **`state.py`**: Declares Pydantic schemas for the shared `WorkflowState`.
*   **`tools.py`**: Numerical Black-Scholes-Merton solver and option Greeks calculator.
*   **`nodes.py`**: Workflow nodes for classification, educational skills, corporate context, options pricing, and response/interaction loop handling.
*   **`agent.py`**: Configures the `Workflow` graph, wiring nodes, edges, and conditional routing.
*   **`skills/`**: Contains the source of truth markdown guidelines (`SKILL.md`) for each individual skill.
*   **`scripts/ingest_pdfs.py`**: Pipeline script to extract, chunk, and embed PDFs into the local ChromaDB database.
*   **`Documents_options/`**: Drop folder for new PDF textbooks and references.

---

## Knowledge Base (Local RAG)

The `documentation_skill` agent uses a local ChromaDB vector database to intelligently search academic papers and option textbooks to answer complex educational queries.

To teach the agent new information:
1. Place any new `.pdf` files into the `Documents_options/` directory.
2. Run the ingestion pipeline from your terminal:
   ```powershell
   uv run python scripts/ingest_pdfs.py
   ```
This will automatically chunk the text, compute embeddings using `gemini-embedding-2`, and save them to the local database located at `skills/documentation_skill/.chroma_db/`. The agent will immediately have access to this new knowledge in your next conversation.

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

Open `.env` and choose one of the following methods:

#### Option A: Google AI Studio API Key (Recommended)
1. Get a key from [Google AI Studio](https://aistudio.google.com/).
2. Uncomment the following lines in `.env` and set your key:
   ```env
   GEMINI_API_KEY="your_api_key"
   GOOGLE_GENAI_USE_VERTEXAI=False
   ```

#### Option B: Google Cloud / Vertex AI
1. Enable the Vertex AI API in the Google Cloud Console.
2. Uncomment the following lines in `.env` and configure your project ID and region:
   ```env
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   GOOGLE_CLOUD_LOCATION="us-central1"
   GOOGLE_GENAI_USE_VERTEXAI=True
   ```
3. Authenticate your terminal session:
   ```powershell
   gcloud auth application-default login
   ```

### 3. Install Dependencies
Run the install command to sync package dependencies:
```powershell
agents-cli install
```

---

## Running the Agent

### Command Line Smoke Test
Run a quick test query from the command line:
```powershell
agents-cli run "What is a call option?"
```

### Interactive Web Playground
Launch the local web-based playground to chat with the agent. 

On Windows (or within PowerShell), run the playground using the direct runner to prevent shell wildcard expansion errors:
```powershell
uv run adk web . --host 127.0.0.1 --port 8080 --reload_agents
```

On Linux/macOS, you can also run:
```bash
agents-cli playground
```

Once started, open your browser and navigate to:
[http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)

This opens the ADK Playground interface, allowing you to test multi-turn conversations and inspect the workflow's state transitions and execution path.
