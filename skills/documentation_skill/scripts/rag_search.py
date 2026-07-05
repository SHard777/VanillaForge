import os
import chromadb
import logging

from google.genai import Client

logger = logging.getLogger(__name__)


def search_options_documentation(query: str) -> str:
    """
    Searches the local ChromaDB for academic definitions and textbook explanations
    regarding options derivatives, the Greeks, and Black-Scholes.
    """
    try:
        # Resolve path to the .chroma_db folder located in the documentation_skill directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(os.path.dirname(current_dir), ".chroma_db")

        if not os.path.exists(db_path):
            return "Knowledge base not initialized. No documents available."

        chroma_client = chromadb.PersistentClient(path=db_path)
        collection = chroma_client.get_collection(name="options_documentation")

        client = Client()
        query_embedding_response = client.models.embed_content(
            model="gemini-embedding-2", contents=query
        )
        query_embedding = query_embedding_response.embeddings[0].values

        results = collection.query(query_embeddings=[query_embedding], n_results=5)

        if results and results.get("documents") and results["documents"][0]:
            retrieved_context = "\n\n---\n\n".join(results["documents"][0])
            logger.info("Successfully retrieved chunks from ChromaDB RAG.")

            # Progressive disclosure: Read SKILL.md and append instructions to the response
            skill_md_path = os.path.join(os.path.dirname(current_dir), "SKILL.md")
            system_instruction = ""
            if os.path.exists(skill_md_path):
                with open(skill_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.startswith("---"):
                        end_idx = content.find("---", 3)
                        if end_idx != -1:
                            system_instruction = content[end_idx + 3 :].strip()
                    else:
                        system_instruction = content.strip()

            return (
                f"Instructions on how to format the answer to the user:\n"
                f"{system_instruction}\n\n"
                f"Retrieved Documentation Results:\n"
                f"{retrieved_context}"
            )

        return "No relevant documentation found for the query."
    except Exception as e:
        logger.error(f"ChromaDB RAG Retrieval failed: {e}")
        return f"Error accessing knowledge base: {e}"
