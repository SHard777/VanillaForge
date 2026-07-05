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

        return {
            "status": "success",
            "ticker": ticker,
            "article_count": len(parsed_articles),
            "articles": parsed_articles
        }

    except Exception as e:
        return {"error": f"Failed to fetch news for '{ticker}': {str(e)}"}
