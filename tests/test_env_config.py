import os
from dotenv import load_dotenv


def test_environment_configuration():
    """
    Verifies that a valid authentication method is set in the .env file.
    """
    # Force load from .env in the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_root, ".env"))

    vertex_flag = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower()
    api_key = os.environ.get("GEMINI_API_KEY")

    if vertex_flag == "true":
        # Option 2: Vertex AI
        assert os.environ.get("GOOGLE_CLOUD_PROJECT"), (
            "GOOGLE_CLOUD_PROJECT must be set when using Vertex AI"
        )
        assert os.environ.get("GOOGLE_CLOUD_LOCATION"), (
            "GOOGLE_CLOUD_LOCATION must be set when using Vertex AI"
        )
    else:
        # Option 1: AI Studio
        assert api_key, "GEMINI_API_KEY must be set if not using Vertex AI"
        assert len(api_key) > 10, "GEMINI_API_KEY appears to be invalid or too short"
