---
name: news_sentiment_skill
description: |
  Retrieves the 10 most recent news articles for a company/ticker and analyzes their sentiment.
  Use this skill when the user asks about "news sentiment", "recent news", or "how the market feels about" a specific publicly traded company or ticker symbol.
  Do NOT use for retrieving historical stock prices or defining financial terms.
version: 1.0.0
---
# News Sentiment Skill

## Purpose & Scope
This skill analyzes recent news sentiment for publicly listed companies. It retrieves the latest 10 news articles for a company, performs a semantic sentiment analysis on each article, identifies key themes, and provides a final aggregated sentiment score.

## Responsibilities
1. **Tool Invocation:** Pass the target company ticker to the `fetch_recent_news` tool.
2. **Output Formatting:** The `fetch_recent_news` tool will perform the full sentiment analysis and return a highly detailed, formatted string containing the article breakdown, company sentiment summary, and final sentiment score.
3. **Response Delivery:** You MUST output the exact text returned by the `fetch_recent_news` tool directly to the user. Do NOT modify or summarize the text, and absolutely do NOT attempt to output any JSON payloads or A2UI blocks yourself. The tool handles all dashboard syncing internally.
