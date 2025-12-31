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

# --- JEEVA AI Style (Deep Dark SaaS) ---
st.markdown("""
<style>
/* Global Reset & Dark Mode */
.stApp {
    background-color: #000000;
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
    background-color: #0A0A0A !important;
    color: #FFFFFF !important;
    border: 1px solid #222 !important;
    border-radius: 12px;
    padding: 20px;
    font-size: 16px;
    text-align: left;
    height: 60px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.stTextInput > div > div > input:focus {
    border-color: #444 !important;
    box-shadow: 0 0 0 2px rgba(255,255,255,0.1);
}

/* Suggestion Pills */
.pill-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}
.pill {
    background-color: #111;
    border: 1px solid #222;
    color: #888;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}
.pill:hover {
    border-color: #444;
    color: #FFF;
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
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Agentic AI for Your Desktop</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Orchestrate complex workflows with autonomous agents.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Command Interface ---
    query = st.text_input("", placeholder="Ask Aether to execute a task...", label_visibility="collapsed")
    
    # --- Suggestion Pills (Visual Only) ---
    st.markdown("""
    <div class="pill-container">
        <div class="pill">Research Company</div>
        <div class="pill">Write Code</div>
        <div class="pill">Analyze Data</div>
        <div class="pill">Find Leads</div>
    </div>
    """, unsafe_allow_html=True)

# --- Result Section ---
if query:
    st.markdown("---")
    
    # Spinner
    with st.spinner("Processing intent..."):
        time.sleep(1.5) # Simulate work
        
    # Mock Report UI
    st.markdown(f"""
    <div class="report-card">
        <div class="report-header">
            <div class="report-title">Mission Report: {query}</div>
            <div class="report-meta">ID: {random.randint(1000,9999)} • {datetime.datetime.now().strftime('%H:%M:%S')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Content Columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Executive Summary")
        st.markdown(f"The system has successfully analyzed the parameters for '**{query}**'. Agents were deployed to gather intelligence and synthesize a strategic response.")
        
        st.markdown("### 🔑 Key Findings")
        st.info("• Signal detected in primary sector.")
        st.info("• Correlation coefficient: 0.98 (High Confidence).")
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
