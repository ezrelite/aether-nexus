import os
import time
import subprocess
from duckduckgo_search import DDGS
from .knowledge import ingest_file, query_knowledge

def study_document(filepath):
    """
    Ingests a document into the Knowledge Base.
    Auto-resolves paths from Desktop/Downloads if needed.
    """
    # 1. Try exact path
    if os.path.exists(filepath):
        return ingest_file(filepath)
        
    # 2. Try expanding Desktop/Downloads using just the FILENAME
    # This fixes hallucinations like "/path/to/secret_plan.txt"
    filename = os.path.basename(filepath)
    user_home = os.path.expanduser("~")
    
    for common_dir in ["Desktop", "Downloads", "Documents"]:
        # Try joining home/Dir/original_path (if relative) AND home/Dir/filename
        paths_to_check = [
            os.path.join(user_home, common_dir, filepath),
            os.path.join(user_home, common_dir, filename)
        ]
        
        for p in paths_to_check:
            if os.path.exists(p):
                return ingest_file(p)
             
    return f"ERROR: File '{filename}' not found on Desktop/Downloads/Documents."

def consult_archive(query):
    """
    Searches the Knowledge Base for answers.
    """
    return query_knowledge(query)

def search_web(query):
    """
    Performs a real web search using DuckDuckGo.
    Retries up to 3 times if no results are found to handle flakiness.
    """
    retries = 3
    for attempt in range(retries):
        try:
            print(f"DEBUG: Search Attempt {attempt+1}/{retries} for '{query}'...") 
            time.sleep(2) # Avoid Rate Limits
            results = DDGS().text(query, max_results=4)
            
            if results:
                 res_str = "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
                 print(f"DEBUG: Found {len(results)} results.")
                 return res_str
            
            print("DEBUG: found 0 results. Retrying...")
            
        except Exception as e:
            print(f"DEBUG: Search error on attempt {attempt+1}: {e}")
            time.sleep(1)
            
    return "No results found after 3 attempts."

def save_file(filename, content):
    """
    Saves a file to the User's Desktop.
    """
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filepath = os.path.join(desktop, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File saved to {filepath}"
    except Exception as e:
        return f"ERROR: Could not save file. {str(e)}"

def open_app(app_name):
    """
    Opens a permitted system application.
    """
    whitelist = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "start chrome" # Uses Windows shell to find default Chrome
    }
    
    cmd = whitelist.get(app_name.lower())
    if not cmd:
        return f"ERROR: App '{app_name}' is not in the whitelist (notepad, calculator, chrome)."
    
    try:
        if app_name.lower() == "chrome":
             # Use shell to let Windows find default browser or chrome
             subprocess.Popen("start chrome", shell=True)
        else:
             subprocess.Popen(cmd)
        return f"SUCCESS: Launched {app_name}."
    except Exception as e:
        return f"ERROR: Failed to launch {app_name}. {str(e)}"

def list_files(path):
    """
    Lists files in a given directory path.
    """
    destinations = {
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    }
    
    # Handle aliases
    clean_path = path.strip().lower().replace("/", "").replace("\\", "")
    if clean_path in destinations:
        path = destinations[clean_path]
    
    # Fuzzy Matching (e.g. "/home/user/Desktop" -> Real Desktop)
    if not os.path.exists(path):
        lower_path = path.lower()
        for key, real_path in destinations.items():
            if key in lower_path: # One last attempt
                path = real_path
                break

    try:
        if not os.path.exists(path):
             return f"Error: Directory '{path}' not found. Try using a full absolute path."
        
        files = os.listdir(path)
        return "\n".join(files) if files else "Directory is empty."
    except Exception as e:
        return f"Error listing files: {str(e)}"
