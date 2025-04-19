import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    """Display detailed model report."""
    # Debug information
    st.write("Debug: Current session state:")
    st.write(st.session_state)
    
    # Add back button at the top
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Back to Analysis"):
            # Clear only specific keys instead of all session state
            keys_to_clear = ['current_page', 'model_report', 'aepf_report', 'report_type']
            for key in keys_to_clear:
                st.session_state.pop(key, None)
            st.session_state['current_page'] = 'Analyser'
            st.rerun()
    
    st.title("Detailed Analysis Report")
    
    # Check which type of report to display
    report_type = st.session_state.get('report_type')
    
    # Handle missing data gracefully
    if report_type == 'model' and not st.session_state.get('model_report'):
        st.error("Model report data is missing. Please return to the Analysis page and try again.")
        return
    elif report_type == 'aepf' and not st.session_state.get('aepf_report'):
        st.error("AEPF report data is missing. Please return to the Analysis page and try again.")
        return
    
    if report_type == 'model':
        show_detailed_model_report()
    elif report_type == 'aepf':
        show_detailed_aepf_report()
    else:
        st.error("No report type specified")

def show_detailed_model_report():
    """Show detailed model analysis report."""
    model_report = st.session_state.get('model_report', {})
    if not model_report:
        st.error("No model report data found")
        return
        
    st.header("AI Model Detailed Analysis")
    
    # Technical Performance
    st.subheader("Technical Performance Metrics")
    tech = model_report.get('technical_analysis', {})
    cols = st.columns(4)
    metrics = {
        "Accuracy": tech.get('accuracy', 0),
        "Precision": tech.get('precision', 0),
        "Recall": tech.get('recall', 0),
        "F1 Score": tech.get('f1_score', 0)
    }
    for col, (metric, value) in zip(cols, metrics.items()):
        col.metric(metric, f"{value:.2%}")
    
    # Example Loans Section
    st.subheader("Recent Loan Examples")
    example_loans = pd.DataFrame({
        'Income': ['$65,000', '$48,000', '$85,000', '$52,000'],
        'Credit Score': [720, 680, 750, 630],
        'DTI Ratio': ['28%', '35%', '22%', '40%'],
        'Loan Amount': ['$200,000', '$150,000', '$300,000', '$175,000'],
        'Decision': ['Approved', 'Approved', 'Approved', 'Denied'],
        'Confidence': ['95%', '82%', '98%', '75%']
    })
    st.dataframe(example_loans, use_container_width=True)
    
    # Risk Distribution
    st.subheader("Risk Distribution Analysis")
    risk_dist = model_report.get('risk_assessment', {}).get('distribution', {})
    fig = go.Figure(data=[go.Pie(labels=list(risk_dist.keys()),
                                values=list(risk_dist.values()),
                                hole=.3)])
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_aepf_report():
    """Show detailed AEPF analysis report."""
    aepf_report = st.session_state.get('aepf_report', {})
    if not aepf_report:
        st.error("No AEPF report data found")
        return
        
    st.header("AEPF Detailed Analysis")
    
    # Overall Scores with star ratings
    st.subheader("Ethical Performance Scores")
    cols = st.columns(3)
    with cols[0]:
        score = aepf_report.get('overall_score', 0)
        stars = "★" * int(score * 5) + "☆" * (5 - int(score * 5))
        st.metric("Overall Score", f"{score:.1%}")
        st.markdown(f"Rating: {stars}")
    
    # Detailed Impact Assessment
    st.subheader("Impact Analysis")
    impact = aepf_report.get('impact_assessment', {})
    for category, score in impact.items():
        st.metric(f"{category} Impact", f"{score:.1%}")
        
    # Recommendations
    st.subheader("Detailed Recommendations")
    st.markdown("""
    1. **Fairness Improvements**
       - Regular bias audits
       - Demographic representation checks
       
    2. **Transparency Measures**
       - Enhanced documentation
       - Clear decision explanations
       
    3. **Risk Mitigation**
       - Continuous monitoring
       - Regular model updates
    """) 