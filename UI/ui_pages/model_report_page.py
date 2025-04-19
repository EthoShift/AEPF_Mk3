import streamlit as st

def show():
    """Show the detailed report."""
    # Back button
    if st.button("← Back"):
        del st.session_state['report_path']
        del st.session_state['current_page']
        st.rerun()
        return

    # Show report
    report_path = st.session_state.get('report_path')
    if report_path:
        try:
            with open(report_path, 'r') as f:
                html = f.read()
            st.components.v1.html(html, height=800, scrolling=True)
        except Exception as e:
            st.error(f"Could not load report: {e}") 