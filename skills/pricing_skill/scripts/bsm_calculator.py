import math
import numpy as np


def std_normal_cdf(x):
    """Computes the Cumulative Distribution Function (CDF) of standard normal distribution."""
    if isinstance(x, (int, float)):
        return 0.5 * (1.0 + math.erf(x / np.sqrt(2.0)))
    
    # Vectorize math.erf for numpy arrays
    vectorized_erf = np.vectorize(math.erf)
    return 0.5 * (1.0 + vectorized_erf(x / np.sqrt(2.0)))


def std_normal_pdf(x):
    """Computes the Probability Density Function (PDF) of standard normal distribution."""
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)


def black_scholes_pricing(
    S: float = None, K: float = 100.0, T: float = 0.5, r: float = 0.04, sigma: float = None, option_type: str = "call", q: float = 0.0, ticker: str = ""
) -> dict:
    """
    Computes the Black-Scholes-Merton option price and Greeks (Delta, Gamma, Theta, Vega, Rho)
    for European Call and Put options.

    Inputs:
        S: Current stock price (underlying). If None and ticker is provided, searches live data.
        K: Strike price
        T: Time to expiration in years (e.g. 0.5 for 6 months)
        r: Risk-free interest rate (as a decimal, e.g. 0.05 for 5%)
        sigma: Implied volatility (as a decimal). If None and ticker is provided, searches live data.
        option_type: "call" or "put" (case-insensitive)
        q: Continuous dividend yield (as a decimal, e.g. 0.02 for 2%)
        ticker: Optional stock ticker (e.g., TSLA) used to fetch live S and sigma if missing.

    Returns:
        dict containing 'price', 'delta', 'gamma', 'theta', 'vega', 'rho'.
    """
    opt_type = option_type.lower().strip()
    if opt_type not in ("call", "put"):
        raise ValueError("option_type must be either 'call' or 'put'")

    date_retrieved = None

    # Sub-Agent Encapsulation: Fetch missing S and sigma via Google Search
    if (S is None or sigma is None) and ticker:
        try:
            from google.genai import Client, types
            import json
            client = Client()
            prompt = (
                f"Find the current live stock price, 30-day At-The-Money (ATM) implied volatility, and the trailing dividend yield for the ticker {ticker}. "
                "Return ONLY a valid JSON object with keys 'S' (spot price as float), 'sigma' (volatility as float, e.g., 0.35), 'q' (dividend yield as float, e.g., 0.042 for 4.2%), and 'date_retrieved' (string, the current date/time the data was found). "
                "Do not include markdown blocks or any other text."
            )
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.0
                )
            )
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:]
            if text.startswith("```"): text = text[3:]
            if text.endswith("```"): text = text[:-3]
            data = json.loads(text.strip())
            if S is None:
                S = float(data.get("S", 100.0))
            if sigma is None:
                sigma = float(data.get("sigma", 0.30))
            if q == 0.0:
                q = float(data.get("q", 0.0))
            date_retrieved = data.get("date_retrieved", None)
        except Exception:
            pass

    # Static Fallbacks if search failed or no ticker was provided
    if S is None:
        S = 100.0
    if sigma is None:
        sigma = 0.30

    # Safeguard against invalid inputs
    S = np.maximum(S, 1e-9)
    K = np.maximum(K, 1e-9)
    sigma = np.maximum(sigma, 1e-9)

    # Expiration check (assuming scalar T for simplicity)
    if np.any(T <= 1e-6):
        # We will handle the scalar case for zero DTE gracefully as before
        if isinstance(T, (int, float)):
            price = max(S - K, 0.0) if opt_type == "call" else max(K - S, 0.0)
            if opt_type == "call":
                delta = 1.0 if S > K else 0.0
            else:
                delta = -1.0 if S < K else 0.0
            result = {
                "price": price,
                "delta": delta,
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0,
                "rho": 0.0,
                "S": S,
                "K": K,
                "T": T,
                "r": r,
                "sigma": sigma,
                "option_type": opt_type,
                "q": q,
            }
            if date_retrieved:
                result["date_retrieved"] = date_retrieved
            return result
        # If T is an array, we could use np.where, but for simplicity of the agent usage, 
        # we will let the normal numpy math continue, since T=1e-9 is protected below.
        T = np.maximum(T, 1e-9)

    # BSM Formula parameters
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate CDF and PDF values
    cdf_d1 = std_normal_cdf(d1)
    cdf_d2 = std_normal_cdf(d2)
    pdf_d1 = std_normal_pdf(d1)

    # Calculate price and Greeks based on type
    if opt_type == "call":
        price = S * np.exp(-q * T) * cdf_d1 - K * np.exp(-r * T) * cdf_d2
        delta = np.exp(-q * T) * cdf_d1
        # Theta for Call
        theta = (
            -(S * np.exp(-q * T) * pdf_d1 * sigma) / (2.0 * np.sqrt(T))
            + q * S * np.exp(-q * T) * cdf_d1
            - r * K * np.exp(-r * T) * cdf_d2
        )
        # Rho for Call
        rho = K * T * np.exp(-r * T) * cdf_d2
    else:  # put
        price = K * np.exp(-r * T) * std_normal_cdf(-d2) - S * np.exp(-q * T) * std_normal_cdf(-d1)
        delta = np.exp(-q * T) * (cdf_d1 - 1.0)
        # Theta for Put
        theta = (
            -(S * np.exp(-q * T) * pdf_d1 * sigma) / (2.0 * np.sqrt(T))
            - q * S * np.exp(-q * T) * std_normal_cdf(-d1)
            + r * K * np.exp(-r * T) * std_normal_cdf(-d2)
        )
        # Rho for Put
        rho = -K * T * np.exp(-r * T) * std_normal_cdf(-d2)

    gamma = (np.exp(-q * T) * pdf_d1) / (S * sigma * np.sqrt(T))
    vega = S * np.exp(-q * T) * np.sqrt(T) * pdf_d1

    result = {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho,
        "S": S,
        "K": K,
        "T": T,
        "r": r,
        "sigma": sigma,
        "option_type": opt_type,
        "q": q,
    }
    if date_retrieved:
        result["date_retrieved"] = date_retrieved
    return result
