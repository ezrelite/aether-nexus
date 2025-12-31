import streamlit as st
import time
import random
import datetime

# --- Configuration ---
st.set_page_config(
    page_title="AETHER NEXUS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- State Management ---
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ""

def set_prompt(text):
    st.session_state['prompt'] = text

# --- JEEVA AI Style (Deep Dark SaaS) ---
st.markdown("""
<style>
/* Global Reset & Dark Mode */
.stApp {
    background-color: #050505; /* Deep Black */
    color: #FFFFFF;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
}

/* Hide Streamlit Elements */
[data-testid="stHeader"] {display: none;}
[data-testid="stSidebar"] {display: none;}
footer {display: none;}

/* Navbar Mock */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #111;
    margin-bottom: 60px;
}
.navbar-brand {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 1px;
}
.navbar-status {
    background-color: #111;
    border: 1px solid #333;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: #00FF99;
}

/* Hero Typography */
.hero-container {
    text-align: center;
    margin-bottom: 40px;
}
.hero-title {
    font-size: 48px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 18px;
    color: #666;
    font-weight: 400;
}

/* Centered Input Styling */
.stTextInput > div > div > input {
    background-color: #111111 !important;
    color: #FFFFFF !important;
    border: 1px solid #333 !important;
    border-radius: 12px;
    padding: 20px;
    font-size: 16px;
    text-align: left;
    height: 60px; /* Taller input */
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.stTextInput > div > div > input:focus {
    border-color: #444 !important;
    box-shadow: 0 0 0 2px rgba(255,255,255,0.1);
}

/* Primary Button (Electric Blue) */
.stButton > button {
    background-color: #0066FF !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 60px;
    font-weight: 600;
    font-size: 16px;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background-color: #0052cc !important;
    box-shadow: 0 0 15px rgba(0, 102, 255, 0.4);
}

/* Suggestion Pills (Styled Buttons) */
/* We target specific buttons by using columns or custom classes if possible, 
   but Streamlit buttons are generic. We'll use a hack or just standard button styling
   that looks different for lighter weights if needed. 
   For now, we will make "Pills" look like secondary buttons. */
div[data-testid="column"] .stButton > button {
    /* If we wanted distinct styles for pills vs primary, we'd need more specific selectors or custom components.
       For now, we'll assume the primary button is in the main column and pills are below.
       Let's use a subtle override logic based on layout if possible, or just style them all cleanly.
       Actually, let's make the Pill buttons Dark Grey. */
    background-color: #1A1A1A !important; 
    border: 1px solid #333 !important;
    color: #B0B0B0 !important;
}
/* But wait, the Primary "EXECUTE" button needs to be Blue. 
   We'll use type="primary" for the Execute button and default for pills. */
button[kind="primary"] {
    background-color: #0066FF !important;
    color: white !important;
    border: none !important;
}
button[kind="secondary"] {
    background-color: #1A1A1A !important;
    border: 1px solid #333 !important;
    color: #B0B0B0 !important;
    border-radius: 20px !important; /* Pill shape */
    height: 40px !important;
}
button[kind="secondary"]:hover {
    border-color: #0066FF !important;
    color: #FFFFFF !important;
}


/* Mission Report Card */
.report-card {
    background-color: #050505;
    border: 1px solid #1A1A1A;
    border-radius: 16px;
    padding: 30px;
    margin-top: 40px;
    animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.report-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    border-bottom: 1px solid #111;
    padding-bottom: 15px;
}
.report-title {
    font-size: 16px;
    font-weight: 600;
    color: #FFF;
}
.report-meta {
    font-size: 12px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# --- Layout: Hidden Navbar ---
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">AETHER_NEXUS</div>
    <div></div>
    <div class="navbar-status">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# --- Layout: Hero Section ---
_, main_col, _ = st.columns([1, 2, 1])

with main_col:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Agentic AI for Your Desktop</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Orchestrate complex workflows with autonomous agents.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Command Interface (2 Columns: Input + Button) ---
    input_col, btn_col = st.columns([4, 1])
    
    with input_col:
        # Binding to session state 'prompt'
        user_input = st.text_input(
            "Command", 
            value=st.session_state['prompt'], 
            placeholder="Ask Aether to execute a task...", 
            label_visibility="collapsed",
            key="widget_prompt"
        )
    
    with btn_col:
        # Primary Action Button
        execute_clicked = st.button("🚀 EXECUTE", type="primary", use_container_width=True)

    # --- Suggestion Pills (Interactive) ---
    # We use 4 columns for pills
    p1, p2, p3, p4 = st.columns(4)
    
    with p1:
        if st.button("🔍 Research Company", use_container_width=True):
            set_prompt("Research [Company Name] and summarize key products")
            st.rerun()
            
    with p2:
        if st.button("💻 Write Code", use_container_width=True):
            set_prompt("Create a Python script to analyze specific data")
            st.rerun()
            
    with p3:
        if st.button("📊 Analyze Data", use_container_width=True):
            set_prompt("Analyze the latest market trends for AI")
            st.rerun()
            
    with p4:
        if st.button("🕵️ Find Leads", use_container_width=True):
            set_prompt("Find potential clients in the SaaS sector")
            st.rerun()

# --- Logic: Execution ---
# Execute if Button Clicked OR (Input is not empty AND it changed/enter pressed logic implied by streamlint reruns)
# Streamlit text_input doesn't have an explicit "on_enter" boolean, but we can check if it has content and if 'execute_clicked'

trigger_execution = False
if execute_clicked and user_input:
    trigger_execution = True
elif user_input and user_input != st.session_state.get('last_executed', ''):
    # This acts as a simple debounce/check if we want to run on enter. 
    # However, standard practice without a form is: button click or explicit instruction.
    # To support "Enter", usually `st.form` is best, but visual requirement is specific.
    # We'll rely on the Button for the explicit "Execute", but if the user wants "Enter" support, 
    # we can treat the text_input's change as a trigger if we update state.
    # For this simplified mock, let's rely on the BUTTON for the main trigger to avoid loopiness,
    # OR trigger anytime the widget text changes and is not empty (which happens on Enter).
    trigger_execution = True

# Update session state to avoid re-running identical prompts instantly
if trigger_execution:
    st.session_state['last_executed'] = user_input
    
    st.markdown("---")
    
    # Spinner
    with st.spinner("Processing intent..."):
        time.sleep(1.2) # Simulate work
        
    # Mock Report UI
    st.markdown(f"""
    <div class="report-card">
        <div class="report-header">
            <div class="report-title">Mission Report: {user_input}</div>
            <div class="report-meta">ID: {random.randint(1000,9999)} • {datetime.datetime.now().strftime('%H:%M:%S')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Content Columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Executive Summary")
        st.markdown(f"The system has successfully analyzed the parameters for '**{user_input}**'. Agents were deployed to gather intelligence and synthesize a strategic response.")
        
        st.markdown("### 🔑 Key Findings")
        st.info("• Signal detected in primary sector.")
        st.info(f"• Target entity '{user_input[:15]}...' identified.")
        st.info("• Architecture validation complete.")
        
    with col2:
        st.markdown("### 📂 Artifacts")
        st.code("report_final.pdf\nanalysis_data.csv\nsource_code.py", language="text")
        
        st.markdown("### ⚙️ Trace")
        st.caption("→ Navigator: Searching...")
        st.caption("→ Architect: Compiling...")
        st.caption("→ Analyst: Verifying...")
        st.success("COMPLETED")
    
    st.markdown("</div>", unsafe_allow_html=True)
