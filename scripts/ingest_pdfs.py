import os
import glob
import chromadb
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai

# Load .env for GEMINI_API_KEY
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))

client = genai.Client()

def embed_text(text: str) -> list[float]:
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    return response.embeddings[0].values

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 300) -> list[str]:
    chunks = []
    start = 0
    text = text.replace("\n", " ").strip() # clean up newlines for better embedding
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def main():
    db_path = os.path.join(project_root, "skills", "documentation_skill", ".chroma_db")
    os.makedirs(db_path, exist_ok=True)
    
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="options_documentation")
    
    pdf_dir = os.path.join(project_root, "Documents_options")
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDFs found in {pdf_dir}")
        return
        
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"\nProcessing {filename}...")
        try:
            reader = PdfReader(pdf_path)
            full_text = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            continue
            
        chunks = chunk_text(full_text)
        print(f"Generated {len(chunks)} chunks.")
        
        # Batching for ChromaDB
        batch_ids = []
        batch_docs = []
        batch_metadatas = []
        batch_embeddings = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            
            # Simple skip check
            existing = collection.get(ids=[chunk_id])
            if existing and existing.get('ids'):
                continue
                
            try:
                embedding = embed_text(chunk)
                batch_ids.append(chunk_id)
                batch_docs.append(chunk)
                batch_metadatas.append({"source": filename})
                batch_embeddings.append(embedding)
            except Exception as e:
                print(f"Error embedding chunk {i}: {e}")
                
        if batch_ids:
            collection.add(
                documents=batch_docs,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            print(f"Added {len(batch_ids)} new chunks to database.")
        else:
            print("No new chunks to add (already in database).")
            
    print("\nIngestion complete!")

if __name__ == "__main__":
    main()
