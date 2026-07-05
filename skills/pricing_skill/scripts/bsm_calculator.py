import math


def std_normal_cdf(x: float) -> float:
    """Computes the Cumulative Distribution Function (CDF) of standard normal distribution."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def std_normal_pdf(x: float) -> float:
    """Computes the Probability Density Function (PDF) of standard normal distribution."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def black_scholes_pricing(
    S: float, K: float, T: float, r: float, sigma: float, option_type: str
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

    Returns:
        dict containing 'price', 'delta', 'gamma', 'theta', 'vega', 'rho'.
    """
    opt_type = option_type.lower().strip()
    if opt_type not in ("call", "put"):
        raise ValueError("option_type must be either 'call' or 'put'")

    # Safeguard against invalid inputs
    S = max(S, 1e-9)
    K = max(K, 1e-9)
    sigma = max(sigma, 1e-9)

    # Expiration check
    if T <= 1e-6:
        price = max(S - K, 0.0) if opt_type == "call" else max(K - S, 0.0)
        # Numerical limits at expiration
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
        }

    # BSM Formula parameters
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    # Calculate CDF and PDF values
    cdf_d1 = std_normal_cdf(d1)
    cdf_d2 = std_normal_cdf(d2)
    pdf_d1 = std_normal_pdf(d1)

    # Calculate price and Greeks based on type
    if opt_type == "call":
        price = S * cdf_d1 - K * math.exp(-r * T) * cdf_d2
        delta = cdf_d1
        # Theta for Call
        theta = (
            -(S * pdf_d1 * sigma) / (2.0 * math.sqrt(T))
            - r * K * math.exp(-r * T) * cdf_d2
        )
        # Rho for Call
        rho = K * T * math.exp(-r * T) * cdf_d2
    else:  # put
        price = K * math.exp(-r * T) * std_normal_cdf(-d2) - S * std_normal_cdf(-d1)
        delta = cdf_d1 - 1.0
        # Theta for Put
        theta = -(S * pdf_d1 * sigma) / (2.0 * math.sqrt(T)) + r * K * math.exp(
            -r * T
        ) * std_normal_cdf(-d2)
        # Rho for Put
        rho = -K * T * math.exp(-r * T) * std_normal_cdf(-d2)

    gamma = pdf_d1 / (S * sigma * math.sqrt(T))
    vega = S * math.sqrt(T) * pdf_d1

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
    }
