import streamlit as st
import os
from pathlib import Path
import pandas as pd
import yaml
import sys
import time
import plotly.graph_objects as go
import logging

# Add project root to Python path
BASE_PATH = Path(__file__).parent.parent
if str(BASE_PATH) not in sys.path:
    sys.path.append(str(BASE_PATH))

# Configure the app
st.set_page_config(
    page_title="AEPF Analysis Platform",
    page_icon="📊",
    layout="wide"
)

# Define available pages for navigation
page_files = {
    "Welcome": os.path.join(BASE_PATH, "UI", "ui_pages", "welcome_page.py"),
    "Analyser": os.path.join(BASE_PATH, "UI", "ui_pages", "analyser.py"),
    "Contact": os.path.join(BASE_PATH, "UI", "ui_pages", "contact.py"),
    "About": os.path.join(BASE_PATH, "UI", "ui_pages", "About.py")
}

# Check for detailed report page first
if st.session_state.get('current_page') == 'detailed_report':
    from ui_pages import detailed_model_report
    detailed_model_report.show()
else:
    # Show normal navigation
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(page_files.keys()))
    
    if selected_page in page_files:
        page_path = page_files[selected_page]
        try:
            if os.path.exists(page_path):
                exec_context = {
                    "__name__": "__main__",
                    "st": st,
                    "os": os,
                    "Path": Path,
                    "pd": pd,
                    "yaml": yaml,
                    "sys": sys,
                    "time": time,
                    "BASE_PATH": BASE_PATH,
                    "__file__": page_path,
                    "go": go,
                    "logging": logging,
                    "logger": logging.getLogger(__name__)
                }
                
                # Clear any existing page content
                st.empty()
                
                with open(page_path, "r", encoding="utf-8") as page_file:
                    content = page_file.read()
                    try:
                        # Execute the content only once
                        exec(content, exec_context)
                        # Call show() only if it exists and hasn't been called
                        if 'show' in exec_context and callable(exec_context['show']):
                            exec_context['show']()
                            # Prevent multiple executions
                            del exec_context['show']
                    except Exception as e:
                        st.error(f"Error executing page: {str(e)}")
        except Exception as e:
            st.error(f"Error loading page '{selected_page}': {str(e)}")
            st.error(f"Full error: {repr(e)}")

# Optional: Add footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Etho Shift")
