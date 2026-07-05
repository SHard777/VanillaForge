import os
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
    assert "Knowledge base not initialized" in result or "No relevant documentation" in result or len(result) > 20

def test_pricing_skill_bsm():
    """
    Tests the BSM calculator tool for standard inputs.
    """
    result = black_scholes_pricing(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2, option_type="call")
    
    assert isinstance(result, dict)
    assert "price" in result
    assert "delta" in result
    # A standard ATM call with these inputs should have a price around $10.45
    assert 10.0 < result["price"] < 11.0

if __name__ == "__main__":
    test_documentation_skill_rag_search()
    test_pricing_skill_bsm()
    print("All tests passed!")
