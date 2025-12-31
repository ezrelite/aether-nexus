import streamlit as st
import requests
import json
import time

# --- Configuration ---
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="AETHER Nexus | Mission Control",
    page_icon="🧠",
    layout="centered", # Chat looks better centered
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (Cyberpunk Aesthetic) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #C0C0C0;
    }
    .stChatInput > div > div > input {
        background-color: #262730;
        color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #00FF99 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .status-badge-online {
        background-color: #00FF99;
        color: black;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-badge-offline {
        background-color: #FF4B4B;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧠 AETHER NEXUS")
with col2:
    # Status Check
    try:
        health = requests.get(f"{API_URL}/", timeout=2)
        if health.status_code == 200:
            st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="status-badge-online">SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="status-badge-offline">SYSTEM ERROR</span></div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="status-badge-offline">DISCONNECTED</span></div>', unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial Greeting
    st.session_state.messages.append({"role": "assistant", "content": "AETHER System Online. Awaiting Mission Objectives."})

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Configuration")
    autonomy = st.selectbox("Autonomy Level", ["high", "low"], index=0, help="High: Can write files/exec code. Low: Read-only.")
    if st.button("Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- Chat Interface ---

# 1. Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # If message has artifacts, show them
        if "artifacts" in msg:
            with st.expander("📂 Mission Artifacts"):
                for artifact in msg["artifacts"]:
                    st.markdown(f"**{artifact['item']}**")
                    st.code(artifact["content"])

# 2. Handle Input
if prompt := st.chat_input("Enter your mission directive..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Execute Mission
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Step A: Thinking
            with st.status("🧠 Cortex Processing...", expanded=True) as status:
                st.write("Analyzing intent...")
                payload = {"intent": prompt, "autonomy_level": autonomy}
                
                start_time = time.time()
                response = requests.post(f"{API_URL}/v1/run", json=payload)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Step B: Log Playback
                    logs = result.get("mission_log", [])
                    for log in logs:
                        st.write(log)
                        time.sleep(0.05) # Aesthetic Typing effect
                    
                    status.update(label=f"✅ Mission Complete ({duration:.2f}s)", state="complete", expanded=False)
                    
                    # Step C: Assistant Reply
                    reply = result.get("assistant_reply", "Mission executed successfully.")
                    message_placeholder.markdown(reply)
                    
                    # Step D: Save to History
                    final_msg = {
                        "role": "assistant", 
                        "content": reply,
                        "artifacts": [] # Simplify for now, could parse real artifacts
                    }
                    
                    # Format Artifacts for History
                    artifacts_data = result.get("artifacts", [])
                    if artifacts_data:
                        st.markdown("---")
                        st.caption("Generated Artifacts:")
                        tabs = st.tabs([f"{a['tool_used']}" for a in artifacts_data])
                        for i, tab in enumerate(tabs):
                            a = artifacts_data[i]
                            with tab:
                                st.code(a.get("output_result", ""))
                                final_msg["artifacts"].append({
                                    "item": a['tool_used'],
                                    "content": a.get("output_result", "")
                                })
                    
                    st.session_state.messages.append(final_msg)
                    
                else:
                    status.update(label="❌ Execution Failed", state="error")
                    error_msg = f"System Error: {response.text}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except Exception as e:
            st.error(f"Connection Error: {e}")
