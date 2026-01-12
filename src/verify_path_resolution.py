"""
Verification Script for Smart Path Resolution.
Tests if study_document("") finds files on Desktop.
"""
from src.tools import study_document

def test_resolution():
    print("--- TESTING SMART PATH ---")
    
    # This file exists on Desktop (verified via dir)
    filename = "secret_plan.txt" 
    
    print(f"Attempting to study '{filename}' (Relative Path)...")
    result = study_document(filename)
    print(f"Result: {result}")
    
    if "SUCCESS" in result:
        print("\nPASS: Automatically found file on Desktop!")
    else:
        print("\nFAIL: Could not resolve path.")

if __name__ == "__main__":
    test_resolution()
