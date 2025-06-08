import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Analysis Details - Log Analyzer AI",
    page_icon="📊",
    layout="wide"
)

# Page Header
st.title("Analysis Details")
st.markdown("Detailed view of log analysis results")

# Get the selected analysis from session state
if 'selected_analysis' not in st.session_state:
    st.session_state.selected_analysis = None

# Analysis Overview
if st.session_state.selected_analysis:
    analysis = st.session_state.selected_analysis
    
    # Overview Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Issues", len(analysis.get('issues', [])))
    with col2:
        high_severity = sum(1 for issue in analysis.get('issues', []) if issue['severity'] == 'High')
        st.metric("High Severity Issues", high_severity)
    with col3:
        st.metric("Analysis Time", analysis.get('timestamp', 'N/A'))
    
    # Summary
    st.markdown("### Analysis Summary")
    st.markdown(analysis.get('summary', 'No summary available'))
    
    # Issues Details
    st.markdown("### Detailed Issues")
    for issue in analysis.get('issues', []):
        with st.expander(f"{issue['description']} ({issue['severity']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Severity:** <span class='severity-{issue['severity'].lower()}'>{issue['severity']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Recommendation:** {issue['recommendation']}")
            with col2:
                st.markdown("**Command to Fix:**")
                st.markdown(f"<div class='command-box'>{issue['command']}</div>", unsafe_allow_html=True)
                st.markdown(f"**Security Implication:** {issue['security_implication']}")
    
    # Export Options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export as JSON"):
            st.download_button(
                "Download JSON",
                json.dumps(analysis, indent=2),
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    with col2:
        if st.button("Export as CSV"):
            df = pd.DataFrame(analysis.get('issues', []))
            st.download_button(
                "Download CSV",
                df.to_csv(index=False),
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Related Issues
    st.markdown("### Related Issues")
    st.info("Related issues will be displayed here based on pattern matching")
    
    # Action Items
    st.markdown("### Recommended Actions")
    for i, issue in enumerate(analysis.get('issues', [])):
        st.checkbox(f"{issue['recommendation']}", key=f"action_{i}")
else:
    st.warning("No analysis selected. Please select an analysis from the Log Analysis page.")

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