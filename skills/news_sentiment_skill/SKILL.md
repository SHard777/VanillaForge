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
This skill analyzes recent news sentiment for publicly listed companies. It retrieves the latest 10 news articles for a company (via an external tool), performs a semantic sentiment analysis on each article, identifies key themes, and provides a final aggregated sentiment score.

## Responsibilities
1. **Tool Invocation:** Pass the target company ticker to the `fetch_recent_news` tool to retrieve the top 10 articles (headline, source, date, URL).
2. **Sentiment Analysis (Per Article):** For each article returned, analyze the headline and assign a sentiment score from 0 to 100 based on the following scale:
   - 0–20 = Very Negative
   - 21–40 = Negative
   - 41–60 = Neutral
   - 61–80 = Positive
   - 81–100 = Very Positive
3. **Thematic Summary:** Analyze the collection of articles to identify key positive themes, negative themes, risks, and opportunities.
4. **Final Scoring:** Compute an overall sentiment score (0-100) for the company based on the aggregate analysis.

## Output Structure
You MUST output the final response exactly according to the following structure:

### 1. Article Breakdown
For each article, display:
- **Headline**: [The article headline]
- **Source**: [The publication source]
- **Date**: [The publication date, if available]
- **Sentiment Score**: [0-100 score]/100
- **Sentiment**: [Classification from the scale above]
- **Rationale**: [Short 1-sentence rationale for why this score was assigned]

### 2. Company Sentiment Summary
Provide a consolidated summary containing:
1. **Key positive themes**
2. **Key negative themes**
3. **Key risks identified**
4. **Key opportunities identified**
5. **A consolidated company sentiment summary**

### 3. Final Sentiment Score
Present the final aggregated score at the very end:
- **Final Sentiment Score**: [0-100 score]/100
- **Classification**: [Classification from the scale above]
- **Summary**: [Brief 1-2 sentence justification for the final score]

## Guidelines for Response Style
- **Tone:** Professional and objective.
- **Constraints:** Do NOT provide investment advice. Clearly distinguish between factual reporting and sentiment interpretation. Cite the news source for every article analyzed.
