import streamlit as st
import requests
import json
import time

# --- Configuration ---
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="AETHER Nexus | Mission Control",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (Cyberpunk Aesthetic) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #C0C0C0;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FFFFFF;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: #FFFFFF;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
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

# --- Sidebar / Header ---
st.title("🧠 AETHER NEXUS")
st.markdown("### Autonomous Executive Task & High-Efficiency Router")

# --- Status Check ---
try:
    health = requests.get(f"{API_URL}/")
    if health.status_code == 200:
        st.markdown('<span class="status-badge-online">SYSTEM ONLINE</span>', unsafe_allow_html=True)
        env_info = health.json().get('env', 'unknown')
        st.caption(f"Environment: {env_info}")
    else:
        st.markdown('<span class="status-badge-offline">SYSTEM ERROR</span>', unsafe_allow_html=True)
except requests.exceptions.ConnectionError:
    st.markdown('<span class="status-badge-offline">SYSTEM OFFLINE</span>', unsafe_allow_html=True)
    st.error("Cannot connect to AETHER Core API. Is `run.py` running?")
    st.stop()

# --- Main Interface ---

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📡 Mission Input")
    intent = st.text_area("Enter Intent / Objective", height=150, placeholder="e.g. Research the latest advancements in solid state batteries and save a summary to report.pdf")
    
    autonomy = st.selectbox("Autonomy Level", ["high", "low"], index=0)
    
    if st.button("EXECUTE MISSION", type="primary"):
        if not intent:
            st.warning("Please enter an intent.")
        else:
            with st.spinner("Nexus Processing..."):
                try:
                    payload = {"intent": intent, "autonomy_level": autonomy}
                    start_time = time.time()
                    response = requests.post(f"{API_URL}/v1/run", json=payload)
                    duration = time.time() - start_time
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state['last_result'] = result
                        st.session_state['last_duration'] = duration
                        st.success(f"Mission Complete ({duration:.2f}s)")
                    else:
                        st.error(f"Execution Failed: {response.text}")
                        with st.expander("Debug details"):
                            st.write(f"Status Code: {response.status_code}")
                            st.write(response.headers)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.warning("Please check if `python run.py` is running and accessible.")

with col2:
    st.subheader("🖥️ Cortex Output")
    
    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        
        # Top Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Status", result['status'])
        m2.metric("Plan ID", result['plan_id'][:8] + "...")
        m3.metric("Artifacts", len(result['artifacts']))
        
        # Artifacts Tabs
        artifacts = result.get('artifacts', [])
        if artifacts:
            tabs = st.tabs([f"{a['tool_used']} ({a['agent_id']})" for a in artifacts])
            
            for i, tab in enumerate(tabs):
                artifact = artifacts[i]
                with tab:
                    st.markdown(f"**Tool:** `{artifact['tool_used']}`")
                    st.markdown(f"**Hash:** `{artifact['verification_hash']}`")
                    
                    st.markdown("#### Input Parameters")
                    st.json(artifact['input_params'])
                    
                    st.markdown("#### Output Result")
                    # Auto-detect if output is code-like or text
                    output = artifact['output_result']
                    if "SUCCESS" in output or "FAILED" in output:
                        st.code(output, language="text")
                    else:
                        st.markdown(output)
        else:
            st.info("No artifacts generated.")
            
        # Raw JSON Expander
        with st.expander("View Raw Protocol JSON"):
            st.json(result)
    else:
        st.info("Ready for input. Awaiting user command.")

# --- Footer ---
st.markdown("---")
st.caption("AETHER Core v0.1.0 | Authorized Personnel Only")
