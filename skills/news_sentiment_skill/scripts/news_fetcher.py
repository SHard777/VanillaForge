import yfinance as yf


def fetch_recent_news(ticker: str) -> dict:
    """
    Retrieves the 10 most recent news articles for a given company ticker using yfinance.
    Returns a dictionary with a list of parsed articles.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        raw_news = ticker_obj.news

        if not raw_news:
            return f"No recent news found for ticker '{ticker}'."

        parsed_articles = []
        for item in raw_news[:10]:
            content = item.get("content", {})
            headline = content.get("title", "Unknown Headline")
            provider = content.get("provider", {})
            source = provider.get("displayName", "Unknown Source")
            date = content.get("pubDate", "Unknown Date")
            parsed_articles.append(f"- **{headline}** ({source}, {date})")

        articles_text = "\n".join(parsed_articles)

        # Now run a nested LLM call to do the sentiment analysis
        from google.genai import Client
        from google.genai import types
        import os
        import json
        import re
        import requests

        client = Client()
        system_instruction = "You are a professional financial analyst. Read the news headlines provided and output a sentiment analysis summary followed by the required JSON block. Do not attempt to use any tools."

        prompt = (
            f"Analyze the sentiment for the following recent news articles about {ticker}:\n\n"
            f"{articles_text}\n\n"
            f"CRITICAL INSTRUCTION: You MUST strictly format your response using the exact 'Output Structure' defined in your system instructions.\n\n"
            f"CRITICAL INSTRUCTION 2: You MUST append the following JSON block at the very end of your response. Fill in the calculated score (-1.0 to 1.0). For the 'headlines' array, you MUST output a list of JSON objects. DO NOT output a list of strings! Each object MUST have exactly three keys: 'text' (the headline string), 'date' (the publication date), and 'sentiment' (one of: 'positive', 'negative', 'neutral').\n"
            f"```json\n"
            f"{{\n"
            f'  "ui_action": "UPDATE_SENTIMENT",\n'
            f'  "data": {{\n'
            f'    "ticker": "{ticker}",\n'
            f'    "score": 0.0,\n'
            f'    "headlines": [\n'
            f'      {{"text": "Example Headline", "date": "2023-10-27", "sentiment": "positive"}}\n'
            f"    ]\n"
            f"  }}\n"
            f"}}\n"
            f"```"
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )

        text = response.text or ""

        # Extreme Robust JSON extraction
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

                # Strip it from text BEFORE the try block
                text_to_strip = text[idx:].strip()
                text = text.replace(text_to_strip, "").strip()
                text = re.sub(r"```json\s*$", "", text).strip()

                try:
                    payload = json.loads(json_str)

                    if "ui_action" not in payload:
                        payload["ui_action"] = "UPDATE_SENTIMENT"
                    if "data" not in payload:
                        payload = {"ui_action": "UPDATE_SENTIMENT", "data": payload}

                    # CRITICAL FIX: Normalize the headlines to ensure 'text' key exists
                    if "headlines" in payload["data"]:
                        normalized_headlines = []
                        for h in payload["data"]["headlines"]:
                            if isinstance(h, str):
                                normalized_headlines.append(
                                    {"text": h, "date": "Today", "sentiment": "neutral"}
                                )
                            elif isinstance(h, dict):
                                headline_str = h.get(
                                    "text",
                                    h.get("headline", h.get("title", "Unknown News")),
                                )
                                h_date = h.get("date", h.get("pubDate", "Today"))
                                h_sentiment = h.get("sentiment", "neutral")
                                normalized_headlines.append(
                                    {
                                        "text": str(headline_str),
                                        "date": str(h_date),
                                        "sentiment": str(h_sentiment),
                                    }
                                )
                        payload["data"]["headlines"] = normalized_headlines

                    # DEBUG LOGGING
                    with open(
                        os.path.join(os.path.dirname(__file__), "debug_payload.json"),
                        "w",
                    ) as df:
                        json.dump(payload, df, indent=2)

                    # Append score and headlines to the text so the Main Agent can output them in the chat window!
                    score_val = payload["data"].get("score", 0.0)
                    display_score = int((score_val + 1.0) * 50.0)
                    text += f"\n\n**Overall Sentiment Score:** {display_score}/100\n\n**Analyzed Headlines:**\n"
                    for h in payload["data"].get("headlines", []):
                        h_text = h.get("text", "Unknown")
                        h_sent = h.get("sentiment", "neutral").upper()
                        text += f"- {h_text} ({h_sent})\n"

                    try:
                        requests.post(
                            "http://localhost:8000/api/internal/a2ui",
                            json=payload,
                            timeout=0.5,
                        )
                    except Exception:
                        pass

                except Exception:
                    pass
        return {"status": "success", "analysis_text": text}

    except Exception as e:
        return {"error": f"Failed to analyze news for '{ticker}': {str(e)}"}
