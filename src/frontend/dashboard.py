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

# 3. CSS INJECTION (The Fix)
st.markdown("""
<style>
    /* GLOBAL THEME */
    .stApp {
        background-color: #050505; /* Deep Black */
        font-family: 'Inter', sans-serif;
    }

    /* INPUT BOX STYLING */
    div[data-testid="stTextInput"] input {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        height: 50px !important;
        padding: 0 15px !important;
    }
    
    /* REMOVE DEFAULT LABELS */
    .stTextInput label {
        display: none !important;
    }

    /* PRIMARY BUTTON STYLING */
    div.stButton > button[kind="primary"] {
        background-color: #0066FF !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: 600 !important;
        
        /* ALIGNMENT FIX: Pushes button down to match input */
        margin-top: 28px !important; 
        
        /* WIDTH FIX: Prevents text wrapping */
        white-space: nowrap !important;
        width: 100% !important;
    }
    
    /* SUGGESTION PILLS */
    div.stButton > button[kind="secondary"] {
        background-color: #1A1A1A !important;
        color: #B0B0B0 !important;
        border: 1px solid #333333 !important;
        border-radius: 30px !important; /* Pill Shape */
        height: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. HEADER
st.markdown("""
<div style="text-align: center; margin-top: 80px; margin-bottom: 40px;">
    <h1 style="font-size: 50px; font-weight: 700; color: white; margin-bottom: 10px;">Agentic AI for Your Desktop</h1>
    <p style="color: #666; font-size: 18px;">Orchestrate complex workflows with autonomous agents.</p>
</div>
""", unsafe_allow_html=True)

# 5. MAIN INTERFACE (Centered)
# We use columns to center the input zone
spacer_left, col_input, col_btn, spacer_right = st.columns([1, 4, 1, 1])

with col_input:
    intent = st.text_input(
        "query", 
        value=st.session_state.prompt,
        placeholder="Ask Aether to execute a task...", 
        label_visibility="collapsed"
    )

with col_btn:
    run_btn = st.button("🚀 EXECUTE", type="primary", use_container_width=True)

# 6. PILLS (Centered)
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) # Spacer
p_spacer_l, p1, p2, p3, p4, p_spacer_r = st.columns([1.5, 1, 1, 1, 1, 1.5])

suggestions = {
    "Research": "Research [Company] and create a SWOT analysis.",
    "Code": "Write a Python script to analyze a CSV file.",
    "Analyze": "Summarize the latest trends in AI agents.",
    "Leads": "Find verified email addresses for CTOs in Fintech."
}

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

# 7. EXECUTION MOCK
if run_btn:
    st.success(f"Starting Mission: {intent}")
