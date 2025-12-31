import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(
    page_title="AETHER NEXUS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SESSION STATE
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""
if 'run_trigger' not in st.session_state:
    st.session_state.run_trigger = False

# 3. CSS - THE "GLASS" THEME
st.markdown("""
<style>
    .stApp { background-color: #050505; font-family: 'Inter', sans-serif; }
    
    /* Hide default streamlit elements we don't want */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* PILL BUTTONS STYLE */
    div.stButton > button[kind="secondary"] {
        background-color: #1A1A1A;
        color: #B0B0B0;
        border: 1px solid #333333;
        border-radius: 50px;
        height: 45px;
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #0066FF;
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 4. HEADER
st.markdown("""
<div style="text-align: center; margin-top: 80px; margin-bottom: 50px;">
    <h1 style="font-size: 60px; font-weight: 700; color: white; margin-bottom: 10px; letter-spacing: -1px;">Agentic AI for Your Desktop</h1>
    <p style="color: #666; font-size: 20px;">Orchestrate complex workflows with autonomous agents.</p>
</div>
""", unsafe_allow_html=True)

# 5. THE MAGIC FORM (PERFECT ALIGNMENT)
# We use a Streamlit Form to keep elements tight
with st.form("aether_command_center", clear_on_submit=False, border=False):
    c1, c2 = st.columns([5, 1], gap="medium")
    
    with c1:
        # Input Box
        user_input = st.text_input(
            "Command", 
            value=st.session_state.prompt, 
            placeholder="Ask Aether to execute a task...", 
            label_visibility="collapsed"
        )
    
    with c2:
        # The Submit Button (Naturally aligned by the Form)
        submitted = st.form_submit_button("🚀 EXECUTE", type="primary", use_container_width=True)

    # Logic: If form submits, update trigger
    if submitted:
        st.session_state.run_trigger = True
        st.session_state.last_prompt = user_input

# 6. SUGGESTION PILLS
# Centered Layout for Pills
st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
_, p1, p2, p3, p4, _ = st.columns([1, 2, 2, 2, 2, 1])

suggestions = {
    "Research": "Research [Company] and create a SWOT analysis.",
    "Code": "Write a Python script to analyze a CSV file.",
    "Analyze": "Summarize the latest trends in AI agents.",
    "Leads": "Find verified email addresses for CTOs in Fintech."
}

# Pill Logic (updates state and reruns)
if p1.button("🔍 Research", type="secondary", use_container_width=True):
    st.session_state.prompt = suggestions["Research"]
    st.rerun()

if p2.button("💻 Code", type="secondary", use_container_width=True):
    st.session_state.prompt = suggestions["Code"]
    st.rerun()

if p3.button("📊 Analyze", type="secondary", use_container_width=True):
    st.session_state.prompt = suggestions["Analyze"]
    st.rerun()

if p4.button("🕵️ Leads", type="secondary", use_container_width=True):
    st.session_state.prompt = suggestions["Leads"]
    st.rerun()

# 7. EXECUTION FEEDBACK
if st.session_state.run_trigger:
    st.markdown("---")
    st.info(f"⚡ **AETHER ONLINE:** Processing command: '{st.session_state.get('last_prompt', '')}'")
    # Reset trigger to prevent loops
    st.session_state.run_trigger = False
