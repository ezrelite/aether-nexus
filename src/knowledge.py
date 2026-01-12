"""
Aether Knowledge Module (The Deep Brain).
Handles RAG (Retrieval Augmented Generation) using ChromaDB and Sentence-Transformers.
OPTIMIZED for HP EliteBook 8440p: Uses 'all-MiniLM-L6-v2' (Small/Fast).
"""
import os

# --- CONFIGURATION ---
DB_PATH = "aether_memory" # Folder for ChromaDB
COLLECTION_NAME = "knowledge_base"
MODEL_NAME = "all-MiniLM-L6-v2"

# --- LAZY SINGLETONS ---
# We store these as None and load them only when needed
_chroma_client = None
_collection = None
_embedder = None

def _get_resources():
    """
    Lazy loader for heavy AI libraries. 
    Prevents Streamlit crash on startup by delaying Torch import.
    """
    global _chroma_client, _collection, _embedder
    
    if _collection is not None and _embedder is not None:
        return _collection, _embedder

    try:
        print("[AETHER]: Loading Deep Brain (Lazy Init)...")
        # Local imports to prevent Streamlit FileWatcher Crash
        import chromadb
        from sentence_transformers import SentenceTransformer
        
        if _chroma_client is None:
            _chroma_client = chromadb.PersistentClient(path=DB_PATH)
            
        if _collection is None:
            _collection = _chroma_client.get_or_create_collection(name=COLLECTION_NAME)
            
        if _embedder is None:
            _embedder = SentenceTransformer(MODEL_NAME)
            
        return _collection, _embedder
        
    except Exception as e:
        print(f"RAG INIT ERROR: {e}")
        return None, None

def ingest_file(filepath):
    """
    Reads a file (PDF/Text), chunks it, and stores embeddings in ChromaDB.
    """
    # Lazy Import for PDF reading
    from pypdf import PdfReader
    
    if not os.path.exists(filepath):
        return f"ERROR: File '{filepath}' not found."
    
    collection, embedder = _get_resources()
    if collection is None:
        return "ERROR: Knowledge Base unavailable."

    try:
        text = ""
        # 1. Extract Text
        if filepath.lower().endswith(".pdf"):
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += str(page.extract_text()) + "\n"
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        
        if not text.strip():
            return "WARNING: File appears empty or unreadable."

        # 2. Chunking (Simple overlap strategy)
        chunk_size = 500
        overlap = 50
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])

        # 3. Embed and Store
        ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filepath, "chunk_id": i} for i in range(len(chunks))]
        
        # SentenceTransformer encodes to lists of floats
        embeddings = embedder.encode(chunks).tolist() 

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return f"SUCCESS: Ingested '{os.path.basename(filepath)}' into Knowledge Base ({len(chunks)} chunks)."

    except Exception as e:
        return f"ERROR: Ingestion failed. {str(e)}"

def query_knowledge(query, n_results=3):
    """
    Semantic search against the Knowledge Base.
    """
    collection, embedder = _get_resources()
    if collection is None:
        return "ERROR: Knowledge Base unavailable."

    try:
        # Embed query
        query_emb = embedder.encode([query]).tolist()
        
        # Search
        results = collection.query(
            query_embeddings=query_emb,
            n_results=n_results
        )
        
        # Format Results
        docs = results['documents'][0]
        sources = results['metadatas'][0]
        
        output = f"### KNOWLEDGE RETRIEVED for '{query}':\n"
        for i, doc in enumerate(docs):
            src = sources[i]['source']
            output += f"- **[Source: {os.path.basename(src)}]**: \"{doc.strip()}...\"\n"
            
        return output

    except Exception as e:
        return f"ERROR: Query failed. {str(e)}"
