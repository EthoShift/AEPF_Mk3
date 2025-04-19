import streamlit as st
from AEPF_Core.report_functions import generate_ethical_analysis_report

def show():
    """Display the report page content."""
    # Back button
    if st.button("← Back to Analysis"):
        st.session_state['selected_page'] = "Analyser"
        st.rerun()

    # Get report type from session state
    report_type = st.session_state.get('report_type')
    
    if report_type == 'ai':
        show_detailed_ai_report()
    elif report_type == 'aepf':
        show_detailed_aepf_report()
    else:
        st.error("No report type specified")

def show_detailed_ai_report():
    """Display detailed AI model report."""
    st.title("Detailed AI Model Analysis")
    model = st.session_state.get('selected_model')
    scenario = st.session_state.get('selected_scenario')
    
    with st.expander("Model Performance", expanded=True):
        st.subheader("Performance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "0.85")
            st.metric("Precision", "0.83")
        with col2:
            st.metric("Recall", "0.87")
            st.metric("F1 Score", "0.85")
    
    with st.expander("Risk Analysis"):
        st.subheader("Risk Factors")
        st.write("Risk analysis for", model, "under", scenario)
        st.metric("Overall Risk Score", "0.32")
    
    with st.expander("Feature Importance"):
        st.subheader("Feature Analysis")
        st.write("Top Features:")
        st.write("- Feature 1: 0.35")
        st.write("- Feature 2: 0.28")
        st.write("- Feature 3: 0.21")

def show_detailed_aepf_report():
    """Display detailed AEPF report."""
    st.title("Detailed AEPF Analysis")
    
    model = st.session_state.get('selected_model')
    scenario = st.session_state.get('selected_scenario')
    report = generate_ethical_analysis_report(model, scenario)
    
    with st.expander("Fairness Analysis", expanded=True):
        st.subheader("Fairness Metrics")
        st.write(f"Overall Fairness Score: {report['fairness_score']:.2f}")
        for metric, value in report['fairness_metrics'].items():
            st.write(f"{metric}: {value:.2f}")
    
    with st.expander("Risk Assessment"):
        st.subheader("Risk Analysis")
        for risk in report['risk_assessment']['risks']:
            st.write(f"**{risk['name']}**")
            st.write(f"Severity: {risk['severity']:.2f}")
            st.write(f"Likelihood: {risk['likelihood']:.2f}")
            st.write(f"Description: {risk['description']}")
    
    with st.expander("Stakeholder Impact"):
        st.subheader("Stakeholder Analysis")
        for stakeholder in report['stakeholder_analysis']['stakeholders']:
            st.write(f"**{stakeholder['name']}**")
            st.write(f"Impact Score: {stakeholder['impact']:.2f}")
            st.write("Key Concerns:")
            for concern in stakeholder['concerns']:
                st.write(f"- {concern}")