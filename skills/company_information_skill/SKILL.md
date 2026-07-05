---
name: company_information_skill
description: |
  Retrieves corporate profiles, business context, sector information, financial metrics, and valuation indicators for publicly listed companies.
  Use this skill when the user asks about what a company does, its competitors, or its financial metrics.
  Do NOT use for pricing options, fetching real-time stock prices, or general derivatives education.
---
# Company Information Skill - Listed Corporate Profile & Market Context
## Purpose & Scope
This skill provides business information, business models, sector context, financial metrics, valuation indicators, and qualitative market analysis for publicly listed corporations.

## Topics to Handle
1.  **Corporate Activities:** What the company does, its core products/services, and its business model.
2.  **Sector & Industry Context:** Competitors, competitive advantage (moats), industry trends, and business environment.
3.  **Market-Related Context:** General perception, business segments (e.g., cloud, hardware, licensing), and corporate history.

4.  **Financials & Valuation Metrics:**
    *   Market Capitalization
    *   Revenue (Annual Turnover) and Fiscal Year End
    *   Gross Profit
    *   EBITDA
    *   Operating Income
    *   Net Income
    *   Earnings Per Share (EPS)
    *   Price-to-Earnings Ratio (P/E or PER)
    *   Dividend Yield
    *   Equity Share Price
    *   Shares Outstanding (when available)

## Guidelines for Response Style
*   **Tone:** Professional yet highly conversational, helpful, and objective.
*   **Audience:** Investors seeking to understand the company behind an option.
*   **Structure:** Present a comprehensive profile of what the company does and address competitive positioning clearly. Follow the Response Structure below meticulously.
*   **Integrity:** Do not provide real-time stock prices (the pricing skill handles numerical options inputs), but do discuss business and financial trends. If specific details are missing, use general financial knowledge to explain the company's market niche.

## Response Structure
Organize the response as follows:
1. Company Overview
2. Business Segments
3. Competitive Position & Industry Context
4. Key Financial Metrics
5. Key Valuation Metrics
6. Investor Takeaways
## Additional Guidance
When financial data is available from the configured market data provider, present the latest available values together with a brief explanation of what each metric means.

When discussing financial metrics:
*   Explain them in plain language suitable for non-technical investors.
*   Distinguish between business quality and valuation.
*   Clearly indicate when information is unavailable or estimated.
*   Prefer factual data retrieval over model-generated estimates.

The skill should provide both qualitative company information and quantitative financial summaries to help users understand the company behind the option.
