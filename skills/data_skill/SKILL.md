---
name: data_skill
description: |
  Retrieves, persists, and visualizes historical market data for equities, ETFs, and indices using yfinance.
  Use this skill when the user asks to "download market data", "fetch historical prices", or "plot a chart" for a given ticker.
  This tool automatically saves the data locally in Parquet format and generates a PNG chart, returning ONLY the file paths to you.
  Do NOT attempt to print the raw dataframe or full dataset to the user; just report the summary and paths provided by the tool.
version: 1.0.0
---
# Data Skill - Historical Market Data & Graphing

## Purpose & Scope
This skill handles the downloading of large historical financial datasets. To preserve your context window (the "Token Budget"), this skill employs the Progressive Disclosure and Decoupled State patterns: it pushes the heavy lifting to a Python script that saves the raw data to disk and only returns lightweight file pointers back to you.

## Responsibilities
1. **Tool Invocation:** Extract the `ticker` (and optionally `start_date` and `end_date`) and pass them to the underlying tool.
2. **Output Formatting:** You will receive a JSON-like summary containing:
   - The original ticker
   - Local paths to the generated `.parquet`, `.png`, and `metadata.json` files
   - Row count and available fields
3. **Response Generation:** Present this summary cleanly to the user. **Do not hallucinate or try to list out the rows.** Instead, confidently state that the data has been securely saved to the file system at the provided paths and provide a brief overview of what was downloaded.

## Guidelines for Response Style
*   **Tone:** Professional and succinct.
*   **Structure:**
    *   Confirm the retrieval.
    *   Present the **Files Created** as a bulleted list.
    *   List the **Rows** and **Available Fields**.
*   **Focus:** Emphasize that the data is ready for their local analysis.
