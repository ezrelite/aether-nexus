import streamlit as st
import json
import warnings
import time

# Suppress Warnings
warnings.filterwarnings("ignore", message=".*renamed to.*", category=RuntimeWarning)
warnings.filterwarnings("ignore", module="duckduckgo_search")

# --- IMPORTS FROM SRC ---
from src.memory_store import load_memory, save_memory
from src.brain import get_groq_response, run_red_team_loop
from src.tools import search_web, save_file, open_app, list_files, study_document, consult_archive

# --- THE UI (Single File Dashboard) ---
st.set_page_config(page_title="AETHER UNIFIED", page_icon="⚡", layout="wide")

# Custom CSS for "Hacker/Dark" Aesthetic
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .stTextInput input { background-color: #262730; color: white; border: 1px solid #4E4E4E; }
    h1 { color: #00FF94; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ AETHER: UNIFIED AGENT")
st.caption(f"Status: ONLINE | Architecture: Modular (v2.0) | Engine: Groq Llama 3")

# Sidebar Configuration
st.sidebar.title("Configuration")

# 1. Model Selector
model_mode = st.sidebar.selectbox(
    "AI Engine Mode",
    ["Auto (Balanced)", "Max Intelligence (Deep Thinker)", "Max Speed (Real-Time)"],
    index=0
)

# Map Selection to ID
if "Max Intelligence" in model_mode:
    selected_model_id = "llama-3.3-70b-versatile"
elif "Max Speed" in model_mode:
    selected_model_id = "llama-3.1-8b-instant"
else:
    # Auto = Speed (for reliability)
    selected_model_id = "llama-3.1-8b-instant"

# 2. Red Team Toggle
red_team_mode = st.sidebar.checkbox("🔴 Activate Red-Team Mode", value=False)
st.sidebar.info("Red-Team Mode triggers a 3-step debate (Builder vs Destroyer) before answering.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- MAIN EXECUTION LOOP ---
if prompt := st.chat_input("Enter command..."):
    # 1. Log User Input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Aether Logic
    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("⚡ *Thinking (Groq Speed)...*")
        
        try:
            # BRANCH: Red Team Mode vs Standard Mode
            if red_team_mode:
                final_answer = run_red_team_loop(prompt, status, model_id=selected_model_id)
                status.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                st.stop() # End execution here for Red Team
                
            # SYSTEM PROMPT: Unified Tool Definition
            current_memory = load_memory()
            system_prompt = f"""
            You are Aether. User Context from Memory: {current_memory}.
            
            ### TOOLS AVAILABLE:
            1. 'SEARCH_WEB': live data/news. Params: query.
            2. 'SAVE_FILE': write files to Desktop. Params: filename, content.
            3. 'OPEN_APP': launch apps (notepad, calc, chrome). Params: app_name.
            4. 'REMEMBER': save user facts. Params: key, value.
            5. 'LIST_FILES': scan folders. Params: path.
            6. 'STUDY_DOCUMENT': read/ingest PDF/TXT. Params: filepath.
            7. 'CONSULT_ARCHIVE': search learned docs. Params: query.
            8. 'NONE': General chat/Answer.
            
            ### INSTRUCTIONS (CHAINING ENABLED):
            - You can take multiple steps to solve a task.
            - IF the user asks for complex research:
              Step 1: SEARCH_WEB (Retry if needed).
              Step 2: Analyze results.
              Step 3: SAVE_FILE or Answer.
            ### INSTRUCTIONS (CHAINING ENABLED):
            - You can take multiple steps to solve a task.
            - IF user asks to *list* files (`LIST_FILES`):
              Step 1: LIST_FILES.
              Step 2: **STOP**. Report the list to the user. Do NOT auto-study.
            - IF user asks about *file content* or specific document (`STUDY_DOCUMENT`):
              Step 1: LIST_FILES to find it (if path unknown).
              Step 2: STUDY_DOCUMENT to ingest it.
              Step 3: CONSULT_ARCHIVE to answer questions.
            - **CRITICAL**: If you see the file in 'LIST_FILES', DO NOT list again. Proceed to STUDY or STOP.
            - **CRITICAL**: Never mention internal tool names (e.g., 'SEARCH_WEB') to the user. Describe capabilities naturally.
            - Return JSON ONLY (This is mandatory).
            
            ### FORMATTING RULES (DYNAMIC):
            - Adapt your response format to the content.
            - For Comparisons: Use Markdown Tables.
            - For Processes: Use Numbered Lists.
            - For Code/Technical: Use Code Blocks.
            - For General Info: Use clean paragraphs with bold highlights.
            - Avoid rigid templates. Be creative and professional.
            
            ### SCHEMA:
            {{
                "thought": "Reasoning...",
                "tool": "SEARCH_WEB" | "SAVE_FILE" | "OPEN_APP" | "REMEMBER" | "LIST_FILES" | "STUDY_DOCUMENT" | "CONSULT_ARCHIVE" | "NONE",
                "query": "...", "filename": "...", "content": "...", "app_name": "...", "key": "...", "value": "...", "path": "...", "filepath": "...",
                "final_reply": "..."
            }}
            """
            
            # --- START MULTI-TURN LOOP ---
            msgs = [{"role": "system", "content": system_prompt}] + \
                   [{"role": "user", "content": m["content"]} for m in st.session_state.messages]
            
            step_count = 0
            max_steps = 5
            
            while step_count < max_steps:
                step_count += 1
                
                # 1. Call Groq
                raw_response = get_groq_response(msgs, model_id=selected_model_id)
                
                try:
                    data = json.loads(raw_response)
                except:
                    # Fallback if model talks instead of JSON
                    data = {"tool": "NONE", "final_reply": raw_response}
                
                tool = data.get("tool")
                thought = data.get("thought", "")
                
                if thought:
                    status.markdown(f"🤔 *{thought}*")
                
                # 2. Execute Tools
                if tool == "SEARCH_WEB":
                    query = data.get("query")
                    status.markdown(f"🌍 *Searching: '{query}'...*")
                    search_res = search_web(query)
                    
                    # Feed result back to memory
                    result_msg = f"TOOL OUT ({tool}): {search_res}"
                    msgs.append({"role": "user", "content": result_msg})
                    
                elif tool == "SAVE_FILE":
                    fname = data.get("filename")
                    content = data.get("content")
                    status.markdown(f"💾 *Saving: {fname}...*")
                    result = save_file(fname, content)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    st.success(result)
                    
                elif tool == "OPEN_APP":
                    app = data.get("app_name")
                    status.markdown(f"🚀 *Launching: {app}...*")
                    result = open_app(app)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    st.success(result)
                    
                elif tool == "REMEMBER":
                    key = data.get("key")
                    val = data.get("value")
                    status.markdown(f"🧠 *Memorizing: {key}...*")
                    result = save_memory(key, val)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    st.info(result)
                    
                elif tool == "LIST_FILES":
                    path = data.get("path")
                    status.markdown(f"📂 *Scanning: {path}...*")
                    result = list_files(path)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    st.write(result) 

                elif tool == "STUDY_DOCUMENT":
                    fpath = data.get("filepath")
                    status.markdown(f"📖 *Reading: {fpath}...*")
                    result = study_document(fpath)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    st.info(result)

                elif tool == "CONSULT_ARCHIVE":
                    query = data.get("query")
                    status.markdown(f"🧠 *Consulting Deep Brain: '{query}'...*")
                    result = consult_archive(query)
                    
                    result_msg = f"TOOL OUT ({tool}): {result}"
                    msgs.append({"role": "user", "content": result_msg})
                    # st.markdown(result) # HIDDEN (User Request)
                
                else: # NONE or Error
                    final_reply = data.get("final_reply", "Task Completed.")
                    status.markdown(final_reply)
                    st.session_state.messages.append({"role": "assistant", "content": final_reply})
                    break # Exit Loop logic

        except Exception as e:
            st.error(f"CRITICAL SYSTEM FAILURE: {e}")
