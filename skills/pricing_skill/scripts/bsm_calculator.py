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
    S, K, T, r, sigma, option_type: str, q: float = 0.0
) -> dict:
    """
    Computes the Black-Scholes-Merton option price and Greeks (Delta, Gamma, Theta, Vega, Rho)
    for European Call and Put options.

    Inputs:
        S: Current stock price (underlying)
        K: Strike price
        T: Time to expiration in years (e.g. 0.5 for 6 months)
        r: Risk-free interest rate (as a decimal, e.g. 0.05 for 5%)
        sigma: Implied volatility (as a decimal, e.g. 0.30 for 30%)
        option_type: "call" or "put" (case-insensitive)
        q: Continuous dividend yield (as a decimal, e.g. 0.02 for 2%)

    Returns:
        dict containing 'price', 'delta', 'gamma', 'theta', 'vega', 'rho'.
    """
    opt_type = option_type.lower().strip()
    if opt_type not in ("call", "put"):
        raise ValueError("option_type must be either 'call' or 'put'")

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
            return {
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

    # Progressive disclosure: Read SKILL.md and append instructions to the response
    import os
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
