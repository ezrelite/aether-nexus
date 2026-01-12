import streamlit as st
import os
import json
from groq import Groq
from duckduckgo_search import DDGS

# --- CONFIGURATION ---
# USER ACTION REQUIRED: You must paste your Groq API Key here
GROQ_API_KEY = "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"

# --- THE BRAIN (Groq Llama 3 - High Speed) ---
def get_groq_response(messages):
    """
    Connects to Groq's high-speed inference engine.
    Uses Llama 3.3 70B (Versatile) for intelligence.
    """
    if "PASTE_YOUR" in GROQ_API_KEY:
        return '{"final_reply": "⚠️ SYSTEM ERROR: Please paste your Groq API Key in the code."}'
        
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

# --- THE HANDS (Web Search) ---
def search_web(query):
    """
    Performs a real web search using DuckDuckGo (No API Key needed).
    Returns the top 3 results summary.
    """
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
    except Exception as e:
        return f"Search Failed: {str(e)}"

# --- THE UI (Single File Dashboard) ---
st.set_page_config(page_title="AETHER RESCUE", page_icon="⚡", layout="wide")

# Custom CSS for "Hacker/Dark" Aesthetic
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .stTextInput input { background-color: #262730; color: white; border: 1px solid #4E4E4E; }
    h1 { color: #00FF94; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ AETHER: RESCUE MODE")
st.caption(f"System Status: ONLINE | Engine: Groq Llama 3 | Latency: Ultra-Low")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- MAIN EXECUTION LOOP ---
if prompt := st.chat_input("Enter command (e.g., 'Research the price of Bitcoin')..."):
    # 1. Log User Input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Aether Logic
    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("⚡ *Thinking (Groq Speed)...*")
        
        try:
            # SYSTEM PROMPT: Forces JSON output for tool use
            system_prompt = """
            You are AETHER. You are an autonomous agent.
            You have access to one tool: 'SEARCH_WEB'.
            
            1. If the user asks a question requiring live data (news, prices, facts), use 'SEARCH_WEB'.
            2. If the user just wants to chat, use 'NONE'.
            
            Return JSON ONLY:
            {
                "thought": "Reasoning here...",
                "tool": "SEARCH_WEB" or "NONE",
                "query": "Search query here (if tool is SEARCH_WEB)",
                "final_reply": "Your final answer to the user (if tool is NONE)"
            }
            """
            
            # Prepare Message History
            msgs = [{"role": "system", "content": system_prompt}] + \
                   [{"role": "user", "content": m["content"]} for m in st.session_state.messages]
            
            # Call Groq (Step 1: Plan)
            raw_response = get_groq_response(msgs)
            
            # Parse JSON
            try:
                data = json.loads(raw_response)
            except:
                # Fallback if model forgets JSON
                data = {"tool": "NONE", "final_reply": raw_response}
            
            # Step 2: Tool Execution
            if data.get("tool") == "SEARCH_WEB":
                query = data["query"]
                status.markdown(f"🌍 *Searching DuckDuckGo for: '{query}'...*")
                
                # Perform Search
                search_data = search_web(query)
                
                # Step 3: Synthesis (Read results and answer)
                synthesis_prompt = f"""
                User Question: {prompt}
                Search Results:
                {search_data}
                
                Based on these results, provide a clear, professional answer.
                IMPORTANT: Return valid JSON ONLY with the key 'final_reply'.
                Example: {{ "final_reply": "Here is what I found..." }}
                """
                final_answer_json = get_groq_response([{"role": "user", "content": synthesis_prompt}])
                
                # Clean up response
                try:
                    final_obj = json.loads(final_answer_json)
                    final_text = final_obj.get("final_reply", str(final_obj))
                except:
                    final_text = final_answer_json
                    
                status.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            
            else:
                # Direct Reply
                reply = data.get("final_reply", "Error parsing response.")
                status.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"CRITICAL SYSTEM FAILURE: {e}")
