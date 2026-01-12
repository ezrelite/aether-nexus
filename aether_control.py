import streamlit as st
import os
import json
import subprocess
from groq import Groq
from duckduckgo_search import DDGS

# --- CONFIGURATION ---
GROQ_API_KEY = "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"

# --- THE BRAIN (Groq Llama 3 - High Speed) ---
def get_groq_response(messages):
    """
    Connects to Groq's high-speed inference engine.
    Uses Llama 3.3 70B (Versatile) for intelligence.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=messages,
            temperature=0.6,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    except Exception as e:
        return json.dumps({"final_reply": f"CONNECTION ERROR: {str(e)}"})

# --- THE HANDS (Tools) ---
def search_web(query):
    """
    Performs a real web search using DuckDuckGo.
    """
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
    except Exception as e:
        return f"Search Failed: {str(e)}"

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

# --- THE UI (Single File Dashboard) ---
st.set_page_config(page_title="AETHER CONTROLLER", page_icon="⚡", layout="wide")

# Custom CSS for "Hacker/Dark" Aesthetic
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .stTextInput input { background-color: #262730; color: white; border: 1px solid #4E4E4E; }
    h1 { color: #00FF94; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ AETHER: SYSTEM CONTROLLER")
st.caption(f"Status: ONLINE | Engine: Groq Llama 3 | Mode: ADMIN (Read/Write/Exec)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- MAIN EXECUTION LOOP ---
if prompt := st.chat_input("Enter command (e.g., 'Open Notepad' or 'Save a poem')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("⚡ *Thinking (Groq Speed)...*")
        
        try:
            # SYSTEM PROMPT: Forces JSON output for tool use
            system_prompt = """
            You are AETHER. You are an autonomous agent with Local System Control.
            
            ### TOOLS AVAILABLE:
            1. 'SEARCH_WEB': Use for live data/news. Params: query.
            2. 'SAVE_FILE': Use to write files to the User's Desktop. Params: filename, content.
            3. 'OPEN_APP': Use to launch apps. Params: app_name (notepad, calculator, chrome).
            4. 'NONE': For general chat.
            
            ### INSTRUCTIONS:
            - If valid JSON cannot be generated, output clear text errors.
            - Return JSON ONLY.
            
            ### SCHEMA:
            {
                "thought": "Reasoning...",
                "tool": "SEARCH_WEB" | "SAVE_FILE" | "OPEN_APP" | "NONE",
                "query": "search query" (for SEARCH_WEB),
                "filename": "name.txt" (for SAVE_FILE),
                "content": "file text" (for SAVE_FILE),
                "app_name": "notepad" (for OPEN_APP),
                "final_reply": "Reply to user" (for NONE)
            }
            """
            
            msgs = [{"role": "system", "content": system_prompt}] + \
                   [{"role": "user", "content": m["content"]} for m in st.session_state.messages]
            
            # Step 1: Plan
            raw_response = get_groq_response(msgs)
            
            try:
                data = json.loads(raw_response)
            except:
                data = {"tool": "NONE", "final_reply": raw_response}
            
            tool = data.get("tool")
            
            # Step 2: Execution
            if tool == "SEARCH_WEB":
                query = data.get("query")
                status.markdown(f"🌍 *Searching DuckDuckGo for: '{query}'...*")
                
                search_data = search_web(query)
                
                synthesis_prompt = f"""
                User Question: {prompt}
                Search Results:
                {search_data}
                
                Based on these results, provide a clear, professional answer.
                IMPORTANT: Return valid JSON ONLY with the key 'final_reply'.
                Example: {{ "final_reply": "Here is what I found..." }}
                """
                final_answer_json = get_groq_response([{"role": "user", "content": synthesis_prompt}])
                
                try:
                    final_obj = json.loads(final_answer_json)
                    final_text = final_obj.get("final_reply", str(final_obj))
                except:
                    final_text = final_answer_json
                    
                status.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                
            elif tool == "SAVE_FILE":
                fname = data.get("filename")
                content = data.get("content")
                status.markdown(f"💾 *Saving to Desktop: {fname}...*")
                
                result = save_file(fname, content)
                
                status.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
                
            elif tool == "OPEN_APP":
                app = data.get("app_name")
                status.markdown(f"🚀 *Launching System App: {app}...*")
                
                result = open_app(app)
                
                status.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
                
            else:
                reply = data.get("final_reply", "Error parsing response.")
                status.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"CRITICAL SYSTEM FAILURE: {e}")
