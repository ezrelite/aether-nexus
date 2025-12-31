import streamlit as st
import time
import random
import datetime
import os

# --- Configuration ---
st.set_page_config(
    page_title="AETHER NEXUS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Loader ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the external stylesheet
css_path = os.path.join(os.path.dirname(__file__), "style.css")
load_css(css_path)

# --- State Management ---
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ""
if 'last_intent' not in st.session_state:
    st.session_state['last_intent'] = ""

def set_prompt(text):
    st.session_state['prompt'] = text

# --- Layout: Navbar ---
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">AETHER_NEXUS</div>
    <div class="navbar-status">
        <div class="status-dot"></div>
        <div class="status-text">SYSTEM ONLINE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Layout: Main Container ---
_, main_col, _ = st.columns([1, 2.5, 1])

with main_col:
    # Typography
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Agentic AI for Your Desktop</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Orchestrate complex workflows with autonomous agents.<br>Enter a command below to initialize the Nexus.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Input Zone (Alignment Fixed) ---
    # Using [4, 1] ratio based on user request for clearer separation and button room
    col_input, col_btn = st.columns([4, 1], gap="small")
    
    with col_input:
        user_input = st.text_input(
            "Command", 
            value=st.session_state['prompt'], 
            placeholder="Ask Aether to execute a task...", 
            key="widget_prompt"
        )
    
    with col_btn:
        run_btn = st.button("EXECUTE", type="primary", use_container_width=True)

    # --- Suggestion Pills (Centered) ---
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    
    # Nested columns for centering the 4 pills
    # layout: 10% space | 20% | 20% | 20% | 20% | 10% space
    p_lead, p1, p2, p3, p4, p_trail = st.columns([0.5, 2, 2, 2, 2, 0.5], gap="small")
    
    with p1:
        if st.button("🔍 Research", use_container_width=True):
            set_prompt("Research [Company Name] and summarize key products")
            st.rerun()
            
    with p2:
        if st.button("💻 Code", use_container_width=True):
            set_prompt("Create a Python script to analyze specific data")
            st.rerun()
            
    with p3:
        if st.button("📊 Analyze", use_container_width=True):
            set_prompt("Analyze the latest market trends for AI")
            st.rerun()
            
    with p4:
        if st.button("🕵️ Leads", use_container_width=True):
            set_prompt("Find potential clients in the SaaS sector")
            st.rerun()

# --- Execution Logic ---
trigger = False

if run_btn:
    trigger = True
elif user_input and user_input != st.session_state['last_intent']:
    trigger = True

if trigger:
    # Update state so we don't re-trigger on simple reruns
    st.session_state['last_intent'] = user_input
    
    st.markdown("---")
    
    # Spinner
    with st.spinner("Initializing autonomous agents..."):
        time.sleep(1.0) 
        
    # Mock Report UI
    st.markdown(f"""
    <div class="report-card">
        <div class="report-header">
            <div class="report-title">Mission Report: {user_input}</div>
            <div class="report-badge">COMPLETED</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📝 Executive Summary")
        st.markdown(f"The system successfully executed the directive '**{user_input}**'. Autonomous agents gathered intelligence from distributed nodes and synthesized the following strategic analysis.")
        
        st.markdown("#### Key Findings")
        st.info("• Primary signal detected in sector 7G.")
        st.info("• Correlation coefficient: 0.98 (High Confidence).")
        st.info("• Architecture validation complete.")
        
    with c2:
        st.markdown("### 📂 Artifacts")
        st.caption("Generated Files:")
        st.code("report_final.pdf\nanalysis_data.csv\nsource_code.py", language="bash")
        
        st.markdown("### ⚙️ Trace")
        st.caption("→ Navigator: Searching...")
        st.caption("→ Architect: Compiling...")
        st.caption("→ Analyst: Verifying...")
    
    st.markdown("</div>", unsafe_allow_html=True)
