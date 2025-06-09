import streamlit as st
import json
from pathlib import Path
import sys
import os
import pandas as pd
from datetime import datetime

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Log Analysis - Linux Log Analyzer Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.log_analyzer import LogAnalyzer

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'username' not in st.session_state:
    st.session_state.username = "Admin"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Log Analysis"
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Custom CSS for styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background-color: {'#0B0C10' if st.session_state.theme == 'dark' else '#F7F9FC'};
        color: {'#ffffff' if st.session_state.theme == 'dark' else '#1B263B'};
    }}
    
    .stApp {{
        background-color: {'#0B0C10' if st.session_state.theme == 'dark' else '#F7F9FC'};
    }}
    
    .header {{
        background-color: {'#1B263B' if st.session_state.theme == 'dark' else '#ffffff'};
        padding: 1rem;
        border-bottom: 1px solid {'#2F3E46' if st.session_state.theme == 'dark' else '#e0e0e0'};
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .logo {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {'#00FFAB' if st.session_state.theme == 'dark' else '#1B263B'};
    }}
    
    .status-card {{
        background-color: {'#1B263B' if st.session_state.theme == 'dark' else '#ffffff'};
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    .status-card h3 {{
        color: {'#00FFAB' if st.session_state.theme == 'dark' else '#1B263B'};
        margin-bottom: 0.5rem;
    }}
    
    .severity-high {{ color: #FF4C4C; }}
    .severity-medium {{ color: #FFA500; }}
    .severity-low {{ color: #4CAF50; }}
    
    .command-box {{
        background-color: {'#2F3E46' if st.session_state.theme == 'dark' else '#f0f2f6'};
        padding: 1rem;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        margin: 0.5rem 0;
    }}
    
    .sidebar {{
        background-color: {'#1B263B' if st.session_state.theme == 'dark' else '#ffffff'};
        padding: 1rem;
    }}
    
    .sidebar-item {{
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    
    .sidebar-item:hover {{
        background-color: {'#2F3E46' if st.session_state.theme == 'dark' else '#f0f2f6'};
    }}
    
    .footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 1rem;
        background-color: {'#1B263B' if st.session_state.theme == 'dark' else '#ffffff'};
        border-top: 1px solid {'#2F3E46' if st.session_state.theme == 'dark' else '#e0e0e0'};
    }}
    
    .linkedin-icon {{
        color: #0077b5;
        font-size: 24px;
        margin-left: 10px;
        text-decoration: none;
    }}
    
    .linkedin-icon:hover {{
        color: #005582;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="logo">🔍 Log Analyzer AI</div>
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="position: relative;">
            <i class="fas fa-bell" style="font-size: 1.2rem;"></i>
            <span style="position: absolute; top: -5px; right: -5px; background-color: #FF4C4C; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem;">3</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-user-circle" style="font-size: 1.5rem;"></i>
            <span>{}</span>
        </div>
    </div>
</div>
""".format(st.session_state.username), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    
    # Theme selection
    new_theme = st.radio("Theme", ["light", "dark"], index=0 if st.session_state.theme == 'light' else 1)
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    st.markdown("---")
    
    # Navigation items
    pages = {
        "Dashboard": "pages/1_Dashboard.py",
        "Log Analysis": "pages/2_Log_Analysis.py",
        "Log Sources": "pages/3_Log_Sources.py",
        "Alerts": "pages/4_Alerts.py"
    }
    
    for page_name in pages.keys():
        if st.button(page_name, use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    st.markdown("---")
    
    # AI Model selection
    st.markdown("### AI Model")
    selected_model = st.session_state.get('selected_model', 'deepseek/deepseek-r1-0528:free')
    model = st.sidebar.selectbox(
        "Select AI Model",
        ["deepseek/deepseek-r1-0528:free", "mistralai/Mistral-7B-Instruct-v0.1"],
        index=0,
        key='selected_model'
    )

# Main content
st.markdown("### Log Analysis")

# File upload or text input
uploaded_file = st.file_uploader("Upload Log File", type=['log', 'txt'])
log_text = st.text_area("Or paste log text here", height=200)

if uploaded_file is not None:
    log_text = uploaded_file.getvalue().decode()

if st.button("Analyze Logs"):
    if log_text:
        try:
            # Create analyzer instance
            analyzer = LogAnalyzer()
            
            # Analyze logs with the selected model
            result = analyzer.analyze_logs(log_text, model=model)
            
            if "error" not in result:
                st.success("Analysis completed successfully!")
                
                # Display summary
                st.markdown("### Summary")
                st.write(result["summary"])
                
                # Display issues
                if result["issues"]:
                    st.markdown("### Issues Found")
                    for issue in result["issues"]:
                        with st.expander(f"{issue['description']} ({issue['severity']})"):
                            st.markdown(f"**Severity:** {issue['severity']}")
                            st.markdown(f"**Recommendation:** {issue.get('recommendation', issue.get('recommendations', [''])[0])}")
                            st.markdown(f"**Command to fix:** {issue.get('command', issue.get('commands', [''])[0])}")
                            st.markdown(f"**Security implication:** {issue.get('security_implication', issue.get('security_implications', [''])[0])}")
                
                # Store analysis in history
                analysis_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "summary": result["summary"],
                    "issues": result["issues"],
                    "model": model
                }
                st.session_state.analysis_history.append(analysis_entry)
            else:
                st.error(f"An error occurred during analysis: {result['error']}")
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
    else:
        st.warning("Please upload a log file or paste log text to analyze.")

# Analysis History
if st.session_state.analysis_history:
    st.markdown("### Analysis History")
    for analysis in reversed(st.session_state.analysis_history):
        with st.expander(f"{analysis['timestamp']} - {analysis['model']}"):
            st.markdown(f"**Summary:** {analysis['summary']}")
            st.markdown("**Issues:**")
            for issue in analysis['issues']:
                st.markdown(f"- {issue['description']} ({issue['severity']})")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Built with Streamlit and AI by Saikiran Mahisakshi
    <a href="https://www.linkedin.com/in/saikiran-mahisakshi-devops/" target="_blank" class="linkedin-icon">
        <i class="fab fa-linkedin"></i>
    </a>
</div>
""", unsafe_allow_html=True)

# Add Font Awesome and other required CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True) 