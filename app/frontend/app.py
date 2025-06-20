import streamlit as st
import json
from pathlib import Path
import sys
import os
import pandas as pd
from datetime import datetime
import base64

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Linux Log Analyzer Agent",
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
    st.session_state.current_page = "Dashboard"

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
    
    .quick-actions {{
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .quick-action-btn {{
        background-color: {'#2F3E46' if st.session_state.theme == 'dark' else '#ffffff'};
        border: 1px solid {'#00FFAB' if st.session_state.theme == 'dark' else '#1B263B'};
        color: {'#00FFAB' if st.session_state.theme == 'dark' else '#1B263B'};
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .quick-action-btn:hover {{
        background-color: {'#00FFAB' if st.session_state.theme == 'dark' else '#1B263B'};
        color: {'#1B263B' if st.session_state.theme == 'dark' else '#ffffff'};
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
    model = st.selectbox(
        "Select AI Model",
        ["deepseek/deepseek-r1-0528:free", "mistralai/Mistral-7B-Instruct-v0.1"],
        index=0
    )

# Main content based on current page
if st.session_state.current_page == "Dashboard":
    st.markdown("### Welcome back, {}".format(st.session_state.username))
    
    # System Overview Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="status-card">
            <h3>Logs Analyzed</h3>
            <p style="font-size: 24px; font-weight: bold;">1,234</p>
            <p style="color: #4CAF50;">↑ 12% from last week</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="status-card">
            <h3>Active Issues</h3>
            <p style="font-size: 24px; font-weight: bold;">23</p>
            <p style="color: #FF4C4C;">↑ 5 new today</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="status-card">
            <h3>System Health</h3>
            <p style="font-size: 24px; font-weight: bold;">98%</p>
            <p style="color: #4CAF50;">All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="status-card">
            <h3>AI Confidence</h3>
            <p style="font-size: 24px; font-weight: bold;">92%</p>
            <p style="color: #4CAF50;">High accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### Quick Actions")
    st.markdown("""
    <div class="quick-actions">
        <button class="quick-action-btn">
            <i class="fas fa-upload"></i> Upload Logs
        </button>
        <button class="quick-action-btn">
            <i class="fas fa-play"></i> Run Analysis
        </button>
        <button class="quick-action-btn">
            <i class="fas fa-bell"></i> Configure Alerts
        </button>
        <button class="quick-action-btn">
            <i class="fas fa-plus"></i> Add Source
        </button>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "Log Analysis":
    st.markdown("### Log Analysis")
    uploaded_file = st.file_uploader("Upload Log File", type=['log', 'txt'])
    log_text = st.text_area("Or paste your logs here:", height=200)
    
    if st.button("Analyze Logs"):
        if uploaded_file is not None:
            log_text = uploaded_file.getvalue().decode()
        elif log_text:
            analyzer = LogAnalyzer()
            result = analyzer.analyze_logs(log_text, model)
            
            if "error" in result:
                st.error(f"Analysis failed: {result['error']}")
            else:
                # Store in history
                if 'analysis_history' not in st.session_state:
                    st.session_state.analysis_history = []
                st.session_state.analysis_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": result.get("summary", ""),
                    "issues": result.get("issues", []),
                    "model": model
                })
                
                # Display results
                st.markdown("### Analysis Results")
                st.markdown(f"**Summary:** {result.get('summary', '')}")
                
                st.markdown("### Issues Found")
                for issue in result.get("issues", []):
                    with st.expander(f"{issue['description']} ({issue['severity']})"):
                        st.markdown(f"**Severity:** <span class='severity-{issue['severity'].lower()}'>{issue['severity']}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Recommendation:** {issue['recommendation']}")
                        st.markdown("**Command to Fix:**")
                        st.markdown(f"<div class='command-box'>{issue['command']}</div>", unsafe_allow_html=True)
                        st.markdown(f"**Security Implication:** {issue['security_implication']}")
                
                # Export options
                st.markdown("### Export Results")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export as JSON"):
                        st.download_button(
                            "Download JSON",
                            json.dumps(result, indent=2),
                            file_name="log_analysis.json",
                            mime="application/json"
                        )
                with col2:
                    if st.button("Export as CSV"):
                        df = pd.DataFrame(result.get("issues", []))
                        st.download_button(
                            "Download CSV",
                            df.to_csv(index=False),
                            file_name="log_analysis.csv",
                            mime="text/csv"
                        )
        else:
            st.warning("Please upload a log file or paste log text to analyze.")

elif st.session_state.current_page == "Log Sources":
    st.markdown("### Log Sources")
    st.markdown("Configure and manage your log sources here.")
    # Add log sources management UI here

elif st.session_state.current_page == "Alerts":
    st.markdown("### Alerts")
    st.markdown("View and manage your alerts here.")
    # Add alerts management UI here

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