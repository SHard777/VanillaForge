import os
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
            return {"error": f"No recent news found for ticker '{ticker}'."}

        parsed_articles = []
        # Get up to 10 articles
        for item in raw_news[:10]:
            content = item.get('content', {})
            
            # Fallbacks in case the yfinance JSON structure changes
            headline = content.get('title', 'Unknown Headline')
            
            provider = content.get('provider', {})
            source = provider.get('displayName', 'Unknown Source')
            
            date = content.get('pubDate', 'Unknown Date')
            
            canonical = content.get('canonicalUrl', {})
            url = canonical.get('url', 'Unknown URL')
            
            parsed_articles.append({
                "headline": headline,
                "source": source,
                "date": date,
                "url": url
            })

        # Progressive disclosure: Read SKILL.md and append instructions to the response
        current_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md_path = os.path.join(os.path.dirname(current_dir), "SKILL.md")
        system_instruction = ""
        if os.path.exists(skill_md_path):
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content.startswith("---"):
                    end_idx = content.find("---", 3)
                    if end_idx != -1:
                        system_instruction = content[end_idx+3:].strip()
                else:
                    system_instruction = content.strip()

        return {
            "__agent_instructions__": f"IMPORTANT: Use the following guidelines to format your response to the user:\n\n{system_instruction}",
            "status": "success",
            "ticker": ticker,
            "article_count": len(parsed_articles),
            "articles": parsed_articles
        }

    except Exception as e:
        return {"error": f"Failed to fetch news for '{ticker}': {str(e)}"}
