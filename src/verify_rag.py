"""
Verification Script for RAG (Phase 24).
"""
import os
import time
from src.knowledge import ingest_file, query_knowledge

def test_rag():
    print("--- STARTING RAG VERIFICATION ---")
    
    # 1. Create Dummy Doc
    test_file = "rag_test_doc.txt"
    content = """
    Project Aether is a unified AI agent.
    It uses Groq Llama 3 for intelligence.
    It stores memory in memory.json.
    Phase 24 added Semantic Search using ChromaDB.
    """
    with open(test_file, "w") as f:
        f.write(content)
        
    print(f"Created {test_file}.")
    
    # 2. Ingest
    print("\n[Test] Ingesting...")
    res = ingest_file(test_file)
    print(res)
    
    if "ERROR" in res:
        print("FAIL: Ingestion failed.")
        return

    # 3. Query
    print("\n[Test] Querying 'semantic search'...")
    answer = query_knowledge("semantic search")
    print(answer)
    
    if "Project Aether" in answer or "ChromaDB" in answer:
        print("\nSUCCESS: RAG is working!")
    else:
        print("\nFAIL: Did not retrieve expected context.")

if __name__ == "__main__":
    try:
        test_rag()
    except Exception as e:
        print(f"CRITICAL FAIL: {e}")
