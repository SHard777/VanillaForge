from skills.documentation_skill.scripts.rag_search import search_options_documentation
from skills.pricing_skill.scripts.bsm_calculator import black_scholes_pricing


def test_documentation_skill_rag_search():
    """
    Tests that the documentation RAG search tool can execute without crashing.
    """
    # We ask a common options question
    result = search_options_documentation("What is a call option?")

    # Verify that the result is a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0

    # We check if it returns either retrieved text or the fallback message
    # if the ChromaDB hasn't been initialized locally
    assert (
        "Knowledge base not initialized" in result
        or "No relevant documentation" in result
        or len(result) > 20
    )


def test_pricing_skill_bsm():
    """
    Tests the BSM calculator tool for standard inputs.
    """
    result = black_scholes_pricing(
        S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, option_type="call"
    )

    assert isinstance(result, dict)
    assert "price" in result
    assert "delta" in result
    # A standard ATM call with these inputs should have a price around $10.45
    assert 10.0 < result["price"] < 11.0


def test_pricing_skill_bsm_dividend():
    """
    Tests the BSM calculator tool for inputs with a continuous dividend yield.
    """
    # A call option on a dividend paying stock should be cheaper than a non-dividend paying stock
    result_no_div = black_scholes_pricing(
        S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, option_type="call"
    )
    result_div = black_scholes_pricing(
        S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, option_type="call", q=0.03
    )

    assert result_div["price"] < result_no_div["price"]
    assert "q" in result_div
    assert result_div["q"] == 0.03


def test_pricing_skill_numpy_array():
    """
    Tests the BSM calculator tool with numpy array inputs to verify vectorization.
    """
    import numpy as np

    S_array = np.array([100.0, 105.0, 110.0])
    K_array = np.array([100.0, 100.0, 100.0])
    T_array = np.array([1.0, 1.0, 1.0])

    result = black_scholes_pricing(
        S=S_array, K=K_array, T=T_array, r=0.05, sigma=0.2, option_type="call"
    )

    assert isinstance(result["price"], np.ndarray)
    assert len(result["price"]) == 3

    # Prices should increase as the stock price goes further in the money
    assert result["price"][0] < result["price"][1] < result["price"][2]


if __name__ == "__main__":
    test_documentation_skill_rag_search()
    test_pricing_skill_bsm()
    test_pricing_skill_bsm_dividend()
    test_pricing_skill_numpy_array()
    print("All tests passed!")
