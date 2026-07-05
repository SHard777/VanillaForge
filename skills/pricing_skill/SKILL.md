---
name: pricing_skill
description: |
  Calculates the Black-Scholes-Merton option price and Greeks (Delta, Gamma, Theta, Vega, Rho) for European Call and Put options.
  Use this skill when the user asks to "price an option" or asks about the numerical value of Greeks given specific inputs (Strike, Spot, Expiry, Volatility).
  CRITICAL: If the user provides a stock ticker (e.g., TSLA) but omits parameters, simply provide the `ticker` parameter to this tool. The tool will automatically perform a secure Google Search internally to find the live Spot Price and Implied Volatility.
  **Static Fallbacks:** If no ticker is provided, or search yields no results, fallback to sensible baselines:
  * Default Stock Price / Strike: $100
  * Default Volatility: 30% (0.30)
  * Default Maturity: 6 months (0.5 years)
  * Default Risk-Free Rate: 4% (0.04)
  Do NOT use for defining what the Greeks mean or for fetching company financial metrics.
---
# Pricing Skill - Vanilla Options Valuation & Greeks Analysis
## Purpose & Scope
This skill is responsible for extracting option pricing parameters from user requests, passing them to the quantitative Black-Scholes-Merton (BSM) calculator, and interpreting the output (option price and Greeks) for the user.

## Responsibilities
1.  **Parameter Extraction:** Identify the inputs required for the Black-Scholes model:
    *   Underlying Asset Price ($S$)
    *   Strike Price ($K$)
    *   Time to Maturity ($T$, in years or converted from days/months)
    *   Risk-free Interest Rate ($r$, as a decimal)
    *   Volatility ($\sigma$, as a decimal)
    *   Option Type (Call or Put)
2.  **Assumption Handling:** 
    *   State all assumptions and any live search results (Spot Price, Implied Volatility) clearly in the output so the user is informed of exactly what inputs were used for the calculation.
3.  **Output Interpretation:** Translate the raw numbers computed by the BSM model:
    *   Explain the resulting option premium.
    *   Explain what the computed Greeks (Delta, Gamma, Theta, Vega, Rho) mean for this specific option.

## Guidelines for Response Style
*   **Tone:** Clear, precise, friendly, and educational.
*   **Structure:** Present the calculation results cleanly. Break down the inputs and output parameters step-by-step.
*   **Visuals:** Use Markdown tables to present inputs, results, and Greeks for readability.
*   **Clarity:** Make sure the distinction between Call and Put options is clear.
