import streamlit as st
import os
import yaml
import logging
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import json

logger = logging.getLogger(__name__)
BASE_PATH = Path(__file__).parent.parent.parent

# Define model-scenario mappings
MODEL_SCENARIOS = {
    "Random Forest": [
        "Candidate Selection",
        "Education Personalization"
    ],
    "Gradient Boosting": [
        "Loan Default Prediction"
    ],
    "Neural Networks": [
        "Medical Treatment Decisions",
        "Customer Support Automation"
    ],
    "Reinforcement Learning": [
        "Autonomous Vehicles"
    ],
    "Linear Programming": [
        "Supply Chain Optimization"
    ],
    "Collaborative Filtering": [
        "Product Recommendation Systems"
    ],
    "Isolation Forest": [
        "Fraud Detection"
    ],
    "Time Series Models": [
        "Energy Consumption Optimization"
    ]
}

def show():
    """Display the analyzer page content."""
    st.title("AI Model Analysis")
    
    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)
    
    with col1:
        # Add "Select..." as first option in model dropdown
        model_options = ["Select..."] + list(MODEL_SCENARIOS.keys())
        model_type = st.selectbox(
            "Select Model Type",
            model_options,
            key="model_selector",
            help="Choose the type of AI model to analyze"
        )
        
        # Only show scenario selection if a model is selected
        if model_type != "Select...":
            available_scenarios = MODEL_SCENARIOS.get(model_type, [])
            scenario = st.selectbox(
                "Select Scenario",
                available_scenarios,
                key="scenario_selector",
                help="Choose the application scenario for analysis"
            )
            
            # Show model description
            model_descriptions = {
                "Random Forest": "Provides interpretability and handles categorical features well.",
                "Gradient Boosting": "Effective for structured data and high-performance classification.",
                "Neural Networks": "Suitable for processing complex data and deep learning tasks.",
                "Reinforcement Learning": "Ideal for decision-making in dynamic environments.",
                "Linear Programming": "Optimized for constraint-based problems.",
                "Collaborative Filtering": "Specialized for recommendation systems.",
                "Isolation Forest": "Designed for anomaly and fraud detection.",
                "Time Series Models": "Tailored for temporal data and forecasting."
            }
            
            if model_type in model_descriptions:
                st.info(f"📚 **{model_type}**: {model_descriptions[model_type]}")
        else:
            st.info("👆 Please select a model type to see available scenarios")

    with col2:
        # AEPF Analysis toggle
        enable_aepf = st.toggle("Enable AEPF Analysis", value=True)
        if enable_aepf:
            st.info("AEPF Analysis is enabled - showing ethical metrics")
    
    # Only show Generate Analysis button if both model and scenario are selected
    if model_type != "Select..." and 'scenario' in locals():
        if st.button("Generate Analysis"):
            st.markdown("### Analysis Results")
            
            # Create columns for side-by-side reports
            report_col1, report_col2 = st.columns(2)
            
            with report_col1:
                st.markdown("### Model Performance")
                
                # Load and display the appropriate report
                if scenario == "Candidate Selection":
                    report_path = Path("AI_Models/Candidate_Selection/outputs/reports/model_report.json")
                    if report_path.exists():
                        with open(report_path) as f:
                            report = json.load(f)
                        
                        # Display metrics with proper formatting
                        metrics = report['metrics']
                        st.metric("Model Accuracy", f"{metrics['accuracy']['value']:.1%}", 
                                 metrics['accuracy']['trend'])
                        st.metric("Precision", f"{metrics['precision']['value']:.1%}", 
                                 metrics['precision']['trend'])
                        st.metric("Recall", f"{metrics['recall']['value']:.1%}", 
                                 metrics['recall']['trend'])
                        
                        # Display feature importance
                        st.markdown("#### Feature Importance")
                        for feature, importance in report['feature_importance'].items():
                            feature_name = feature.replace('_', ' ').title()
                            st.progress(importance, text=f"{feature_name}: {importance:.1%}")
                        
                        # Display recent decisions table
                        st.markdown("#### Recent Model Decisions")
                        decisions_df = pd.DataFrame({
                            'ID': ['A001', 'A002', 'A003', 'A004'],
                            'Position': ['Senior Dev', 'Data Scientist', 'ML Engineer', 'DevOps Lead'],
                            'Experience': ['8 years', '5 years', '6 years', '7 years'],
                            'Tech Score': ['92%', '88%', '85%', '90%'],
                            'Decision': ['Selected', 'Interview', 'Selected', 'Interview'],
                            'Confidence': ['95%', '87%', '92%', '89%']
                        })
                        
                        st.dataframe(
                            decisions_df,
                            column_config={
                                'Tech Score': st.column_config.ProgressColumn(
                                    'Technical Assessment',
                                    help='Technical evaluation score',
                                    format='%s',
                                    min_value=0,
                                    max_value=100,
                                ),
                                'Confidence': st.column_config.ProgressColumn(
                                    'Model Confidence',
                                    help='AI confidence in decision',
                                    format='%s',
                                    min_value=0,
                                    max_value=100,
                                )
                            },
                            hide_index=True
                        )
                        
                        # Display insights
                        st.markdown("#### Key Insights")
                        st.write("Strengths:")
                        for strength in report['insights']['strengths']:
                            st.write(f"✓ {strength}")
                            
                        st.write("Areas for Improvement:")
                        for area in report['insights']['improvement_areas']:
                            st.write(f"• {area}")
                    else:
                        st.warning(f"No report found at {report_path}")
                elif scenario == "Loan Default Prediction":
                    # Get absolute path to project root
                    current_file = Path(__file__).resolve()
                    project_root = current_file.parent.parent.parent
                    
                    # Construct report path
                    report_path = project_root / 'AI_Models/Loan_default/outputs/reports/model_report.json'
                    print(f"Looking for report at: {report_path.absolute()}")  # Debug print
                    
                    if not report_path.exists():
                        # Try to generate report
                        try:
                            from AI_Models.Loan_default.scripts.generate_initial_report import create_initial_report
                            create_initial_report()
                            print("Generated new report")
                        except Exception as e:
                            print(f"Error generating report: {e}")
                    
                    if report_path.exists():
                        print("Found report file")  # Debug print
                        try:
                            with open(report_path) as f:
                                report = json.load(f)
                                print("Successfully loaded report")  # Debug print
                            
                            # Display metrics with explanations
                            metrics = report['metrics']
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Model Accuracy", f"{metrics['accuracy']['value']:.1%}", 
                                         metrics['accuracy']['trend'])
                                st.markdown("*Overall prediction accuracy*")
                            
                            with col2:
                                st.metric("Default Detection", f"{metrics['precision']['value']:.1%}", 
                                         metrics['precision']['trend'])
                                st.markdown("*Accuracy in identifying defaults*")
                            
                            with col3:
                                st.metric("Risk Assessment", f"{metrics['recall']['value']:.1%}", 
                                         metrics['recall']['trend'])
                                st.markdown("*Completeness of risk capture*")
                            
                            # Display risk distribution
                            st.markdown("#### Risk Distribution")
                            risk_data = pd.DataFrame({
                                'Category': ['Low Risk', 'Medium Risk', 'High Risk'],
                                'Percentage': [60, 30, 10]
                            })
                            
                            fig = go.Figure(data=[go.Pie(labels=risk_data['Category'], 
                                                        values=risk_data['Percentage'],
                                                        hole=.3)])
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Display feature importance
                            st.markdown("#### Feature Importance")
                            for feature, importance in report['feature_importance'].items():
                                feature_name = feature.replace('_', ' ').title()
                                st.progress(importance, text=f"{feature_name}: {importance:.1%}")
                            
                            # Display recent decisions table
                            st.markdown("#### Recent Model Decisions")
                            decisions_df = pd.DataFrame({
                                'ID': ['A001', 'A002', 'A003', 'A004'],
                                'Position': ['Senior Dev', 'Data Scientist', 'ML Engineer', 'DevOps Lead'],
                                'Experience': ['8 years', '5 years', '6 years', '7 years'],
                                'Tech Score': ['92%', '88%', '85%', '90%'],
                                'Decision': ['Selected', 'Interview', 'Selected', 'Interview'],
                                'Confidence': ['95%', '87%', '92%', '89%']
                            })
                            
                            st.dataframe(
                                decisions_df,
                                column_config={
                                    'Tech Score': st.column_config.ProgressColumn(
                                        'Technical Assessment',
                                        help='Technical evaluation score',
                                        format='%s',
                                        min_value=0,
                                        max_value=100,
                                    ),
                                    'Confidence': st.column_config.ProgressColumn(
                                        'Model Confidence',
                                        help='AI confidence in decision',
                                        format='%s',
                                        min_value=0,
                                        max_value=100,
                                    )
                                },
                                hide_index=True
                            )
                            
                            # Display insights
                            st.markdown("#### Key Insights")
                            st.write("Strengths:")
                            for strength in report['insights']['strengths']:
                                st.write(f"✓ {strength}")
                                
                            st.write("Areas for Improvement:")
                            for area in report['insights']['improvement_areas']:
                                st.write(f"• {area}")
                            
                            # Display recent loan decisions
                            st.markdown("#### Recent Loan Decisions")
                            loan_data = pd.DataFrame({
                                'Loan ID': ['L001', 'L002', 'L003'],
                                'Amount': ['$50,000', '$75,000', '$100,000'],
                                'Risk Score': ['Low', 'Medium', 'High'],
                                'Decision': ['Approved', 'Pending', 'Rejected'],
                                'Confidence': ['95%', '82%', '91%']
                            })
                            st.dataframe(loan_data, hide_index=True)
                        except Exception as e:
                            print(f"Error loading/displaying report: {e}")
                            st.error(f"Error displaying report: {e}")
                    else:
                        print(f"Report file not found at {report_path}")
                        st.warning(f"No report found at {report_path}")
                else:
                    st.info(f"Report generation for {scenario} is under development.")
                
            with report_col2:
                if enable_aepf:
                    st.markdown("### Ethical Analysis")
                    if scenario == "Candidate Selection":
                        # Overall Rating with stars
                        overall_score = 0.85
                        star_rating = min(5, max(1, round(overall_score * 5)))
                        stars = "★" * star_rating + "☆" * (5 - star_rating)
                        
                        styled_stars = f"""
                            <span style="
                                color: gold;
                                font-size: 40px;
                                letter-spacing: 5px;
                                font-weight: bold;
                                text-shadow: 0px 0px 1px #000;
                            ">
                                {stars}
                            </span>
                        """
                        st.markdown(styled_stars, unsafe_allow_html=True)
                        st.markdown(f"#### Overall Ethical Score: {overall_score:.0%}")
                        st.markdown("---")
                        
                        # Decision Analysis Example - moved outside expander
                        st.markdown("### 🔍 Recent Decision Analysis")
                        st.markdown("""
                            #### Decision Context
                            - **Position**: Senior Software Developer
                            - **Applicants**: 150 candidates
                            - **Key Requirements**: Technical expertise, leadership potential, team fit
                            
                            #### Model Decision Process
                            1. **Initial Screening**
                               - 85 candidates met technical requirements
                               - Bias mitigation applied to technical assessment
                               - Diverse candidate pool maintained
                            
                            2. **Detailed Evaluation**
                               - Leadership potential assessed through behavioral indicators
                               - Team compatibility evaluated using cultural alignment metrics
                               - Experience validation with bias-aware scoring
                            
                            3. **Final Selection**
                               - Top 5 candidates identified
                               - Demographic parity verified
                               - Decision explanations generated
                        """)
                        
                        # Fairness Metrics with Context
                        st.markdown("### 📊 Fairness Analysis")
                        fairness_metrics = {
                            "Demographic Parity": (0.85, "Balanced representation across groups"),
                            "Equal Opportunity": (0.82, "Fair advancement chances for qualified candidates"),
                            "Disparate Impact": (0.88, "Minimal adverse effects on protected groups")
                        }
                        for metric, (value, description) in fairness_metrics.items():
                            st.metric(metric, f"{value:.0%}")
                            st.markdown(f"*{description}*")
                            st.markdown("---")
                        
                        # Ethical Considerations
                        st.markdown("### 🎯 Ethical Impact Analysis")
                        st.markdown("""
                            #### Positive Outcomes
                            - **Diversity Enhancement**: 20% increase in team diversity
                            - **Skill Objectivity**: Standardized technical assessment
                            - **Transparency**: Clear feedback provided to all candidates
                            
                            #### Areas for Attention
                            - **Experience Bias**: Monitoring impact of years of experience
                            - **Cultural Fit**: Ensuring objective assessment
                            - **Interview Process**: Standardizing panel composition
                        """)
                        
                        # Recommendations with Context - more concise version
                        st.markdown("### 💡 Ethical Recommendations")
                        with st.expander("View Recommendations"):
                            recommendations = [
                                {
                                    "title": "Bias Mitigation",
                                    "details": "Unconscious bias checks in assessments",
                                    "impact": "High",
                                    "timeline": "3mo"
                                },
                                {
                                    "title": "Group Monitoring",
                                    "details": "Track selection rates by demographics",
                                    "impact": "Med",
                                    "timeline": "Ongoing"
                                },
                                {
                                    "title": "Fairness Audits",
                                    "details": "Review decision patterns",
                                    "impact": "High",
                                    "timeline": "Q"
                                }
                            ]
                            
                            # Compact table display
                            rec_df = pd.DataFrame(recommendations)
                            st.dataframe(
                                rec_df,
                                column_config={
                                    "title": "Recommendation",
                                    "details": "Details",
                                    "impact": st.column_config.TextColumn(
                                        "Impact",
                                        width="small"
                                    ),
                                    "timeline": st.column_config.TextColumn(
                                        "When",
                                        width="small"
                                    )
                                },
                                hide_index=True
                            )

                        # Display ethical analysis of decisions
                        st.markdown("### 🔍 Decision Ethics Analysis")
                        ethics_df = pd.DataFrame({
                            'ID': ['A001', 'A002', 'A003', 'A004'],
                            'Decision': ['Selected', 'Interview', 'Selected', 'Interview'],
                            'Fairness': ['95%', '92%', '94%', '93%'],
                            'Bias Risk': ['Low', 'Low', 'Low', 'Low'],
                            'Protected Groups': ['Balanced', 'Balanced', 'Balanced', 'Balanced'],
                            'Transparency': ['High', 'High', 'High', 'High']
                        })
                        
                        st.dataframe(
                            ethics_df,
                            column_config={
                                'Fairness': st.column_config.ProgressColumn(
                                    'Fairness Score',
                                    help='Overall fairness rating',
                                    format='%s',
                                    min_value=0,
                                    max_value=100,
                                ),
                                'Bias Risk': st.column_config.SelectboxColumn(
                                    'Bias Risk Level',
                                    help='Potential bias risk assessment',
                                    width='small',
                                    options=['Low', 'Medium', 'High']
                                ),
                                'Protected Groups': st.column_config.SelectboxColumn(
                                    'Group Impact',
                                    help='Impact on protected groups',
                                    width='medium',
                                    options=['Balanced', 'Review Needed', 'Imbalanced']
                                )
                            },
                            hide_index=True
                        )
                    elif scenario == "Loan Default Prediction":
                        # Overall Rating with stars
                        overall_score = 0.87
                        star_rating = min(5, max(1, round(overall_score * 5)))
                        stars = "★" * star_rating + "☆" * (5 - star_rating)
                        
                        styled_stars = f"""
                            <span style="
                                color: gold;
                                font-size: 40px;
                                letter-spacing: 5px;
                                font-weight: bold;
                                text-shadow: 0px 0px 1px #000;
                            ">
                                {stars}
                            </span>
                        """
                        st.markdown(styled_stars, unsafe_allow_html=True)
                        st.markdown(f"#### Overall Ethical Score: {overall_score:.0%}")
                        st.markdown("---")
                        
                        # Fairness Metrics
                        st.markdown("### 📊 Fairness Analysis")
                        fairness_metrics = {
                            "Equal Treatment": (0.88, "Fair lending across demographics"),
                            "Risk Assessment": (0.85, "Balanced risk evaluation"),
                            "Approval Equity": (0.86, "Consistent approval rates")
                        }
                        for metric, (value, description) in fairness_metrics.items():
                            st.metric(metric, f"{value:.0%}")
                            st.markdown(f"*{description}*")
                            st.markdown("---")
                        
                        # Ethical Impact
                        st.markdown("### 🎯 Ethical Impact")
                        st.markdown("""
                            #### Positive Outcomes
                            - **Fair Access**: Equal loan opportunities
                            - **Risk Balance**: Objective assessment
                            - **Transparency**: Clear decision criteria
                            
                            #### Areas for Attention
                            - **Income Bias**: Monitor income group impact
                            - **Credit History**: Fair evaluation
                            - **Documentation**: Clear requirements
                        """)
                        
                        # Recommendations with Context - more concise version
                        st.markdown("### 💡 Ethical Recommendations")
                        with st.expander("View Recommendations"):
                            recommendations = [
                                {
                                    "title": "Risk Assessment",
                                    "details": "Regular fairness audits of risk scoring",
                                    "impact": "High",
                                    "timeline": "Q"
                                },
                                {
                                    "title": "Demographic Monitoring",
                                    "details": "Track approval rates across groups",
                                    "impact": "High",
                                    "timeline": "Monthly"
                                },
                                {
                                    "title": "Documentation",
                                    "details": "Improve decision transparency",
                                    "impact": "Med",
                                    "timeline": "Ongoing"
                                }
                            ]
                            
                            # Compact table display
                            rec_df = pd.DataFrame(recommendations)
                            st.dataframe(
                                rec_df,
                                column_config={
                                    "title": "Recommendation",
                                    "details": "Details",
                                    "impact": st.column_config.TextColumn(
                                        "Impact",
                                        width="small"
                                    ),
                                    "timeline": st.column_config.TextColumn(
                                        "When",
                                        width="small"
                                    )
                                },
                                hide_index=True
                            )

def show_model_summary(report: dict):
    """Display AI model summary metrics."""
    try:
        scenario_type = report.get('scenario_type', 'Loan Default')
        
        # Load the AI model report
        model_report = load_model_report(scenario_type)
        if model_report:
            report = model_report  # Use the loaded report instead of merging
        
        st.markdown("### AI Model Report")
        
        if scenario_type == "Candidate Selection":
            # Model Overview
            st.markdown(f"""
                #### {report.get('model_type', 'Neural Network Recruitment Model')}
                This AI model analyzes candidate profiles using multiple factors to predict hiring success 
                and evaluate candidate suitability.
            """)
            
            # Performance Metrics
            metrics = report.get('metrics', {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                accuracy = metrics.get('accuracy', {})
                st.metric(
                    "Model Accuracy",
                    f"{accuracy.get('value', 0):.0%}",
                    accuracy.get('trend', '')
                )
                st.markdown(f"*{accuracy.get('narrative', '')}*")
            
            with col2:
                precision = metrics.get('precision', {})
                st.metric(
                    "Selection Precision",
                    f"{precision.get('value', 0):.0%}",
                    precision.get('trend', '')
                )
                st.markdown(f"*{precision.get('narrative', '')}*")
            
            with col3:
                recall = metrics.get('recall', {})
                st.metric(
                    "Candidate Recall",
                    f"{recall.get('value', 0):.0%}",
                    recall.get('trend', '')
                )
                st.markdown(f"*{recall.get('narrative', '')}*")
            
            # Feature Importance
            st.markdown("### Feature Impact Analysis")
            feature_importance = report.get('feature_importance', {})
            
            fig = go.Figure([go.Bar(
                x=list(feature_importance.keys()),
                y=list(feature_importance.values()),
                marker_color='royalblue'
            )])
            fig.update_layout(
                title='Feature Importance in Decision Making',
                yaxis_title='Impact Score',
                xaxis_title='Features'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent Decisions
            st.markdown("### Recent Model Decisions")
            for decision in report.get('decisions', []):
                with st.expander(f"🎯 {decision['position']}"):
                    st.markdown(f"""
                        #### Decision Analysis
                        **Profile Scores:**
                        - Technical Skills: {decision['profile']['technical_skills']}/100
                        - Communication: {decision['profile']['communication_skills']}/100
                        - Leadership: {decision['profile']['leadership_skills']}/100
                        - Cultural Fit: {decision['profile']['cultural_fit']}/100
                        
                        **Model Confidence:** {decision['confidence']:.0%}
                        
                        **Key Factors:**
                        {chr(10).join([f'- {factor}' for factor in decision['key_factors']])}
                        
                        **Uncertainty Areas:**
                        {chr(10).join([f'- {factor}' for factor in decision.get('uncertainties', [])])}
                    """)
            
            # Performance Trends
            st.markdown("### Performance Analysis")
            trends = report.get('performance_trends', {})
            
            trend_data = pd.DataFrame({
                'Area': list(trends.keys()),
                'Accuracy': [t['accuracy'] for t in trends.values()],
                'Confidence': [t['confidence'] for t in trends.values()]
            })
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                name='Accuracy',
                x=trend_data['Area'],
                y=trend_data['Accuracy'],
                marker_color='royalblue'
            ))
            fig2.add_trace(go.Bar(
                name='Confidence',
                x=trend_data['Area'],
                y=trend_data['Confidence'],
                marker_color='lightgreen'
            ))
            fig2.update_layout(
                title='Model Performance by Assessment Area',
                barmode='group'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Insights
            st.markdown("### Model Insights")
            insights = report.get('insights', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Strengths")
                for strength in insights.get('strengths', []):
                    st.markdown(f"- {strength}")
            
            with col2:
                st.markdown("#### Areas for Improvement")
                for area in insights.get('improvement_areas', []):
                    st.markdown(f"- {area}")
            
            # Add Candidate Case Studies
            st.markdown("### 👥 Candidate Case Studies")
            
            case_studies = [
                {
                    "id": "CS001",
                    "role": "Senior Software Engineer",
                    "profile": {
                        "years_exp": 8,
                        "tech_stack": ["Python", "React", "AWS"],
                        "scores": {
                            "technical": 92,
                            "communication": 88,
                            "leadership": 85,
                            "cultural_fit": 90
                        }
                    },
                    "decision": "Selected",
                    "key_strengths": [
                        "Strong system design experience",
                        "Team leadership background",
                        "Open source contributions"
                    ],
                    "areas_for_growth": [
                        "Enterprise architecture exposure",
                        "Cross-functional collaboration"
                    ],
                    "model_confidence": 0.94
                },
                {
                    "id": "CS002",
                    "role": "Data Scientist",
                    "profile": {
                        "years_exp": 5,
                        "tech_stack": ["Python", "TensorFlow", "SQL"],
                        "scores": {
                            "technical": 89,
                            "communication": 92,
                            "leadership": 78,
                            "cultural_fit": 88
                        }
                    },
                    "decision": "Interview Stage",
                    "key_strengths": [
                        "ML model deployment experience",
                        "Strong analytical skills",
                        "Research background"
                    ],
                    "areas_for_growth": [
                        "Production system experience",
                        "Project management skills"
                    ],
                    "model_confidence": 0.87
                }
            ]
            
            for case in case_studies:
                with st.expander(f"📋 {case['role']} (ID: {case['id']})"):
                    # Profile Overview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Profile Overview")
                        st.markdown(f"""
                            - **Experience**: {case['profile']['years_exp']} years
                            - **Tech Stack**: {', '.join(case['profile']['tech_stack'])}
                            - **Decision**: {case['decision']}
                            - **Model Confidence**: {case['model_confidence']:.0%}
                        """)
                    
                    with col2:
                        # Radar chart for scores
                        scores = case['profile']['scores']
                        fig = go.Figure(data=go.Scatterpolar(
                            r=[scores['technical'], scores['communication'], 
                               scores['leadership'], scores['cultural_fit']],
                            theta=['Technical', 'Communication', 
                                   'Leadership', 'Cultural Fit'],
                            fill='toself',
                            name='Skills Assessment'
                        ))
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Strengths and Growth Areas
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Key Strengths")
                        for strength in case['key_strengths']:
                            st.markdown(f"✓ {strength}")
                    
                    with col2:
                        st.markdown("#### Areas for Growth")
                        for area in case['areas_for_growth']:
                            st.markdown(f"• {area}")
                    
                    # Model Analysis
                    st.markdown("#### Model Analysis")
                    st.progress(case['model_confidence'], 
                              text=f"Model Confidence: {case['model_confidence']:.0%}")
                    
                    # Decision Factors
                    st.markdown("#### Key Decision Factors")
                    factors = {
                        "Technical Expertise": scores['technical'] / 100,
                        "Team Fit": scores['cultural_fit'] / 100,
                        "Growth Potential": scores['leadership'] / 100,
                        "Communication": scores['communication'] / 100
                    }
                    
                    for factor, value in factors.items():
                        st.progress(value, text=f"{factor}: {value:.0%}")
            
            # Add comparison view
            st.markdown("### 📊 Candidate Comparison")
            comparison_df = pd.DataFrame([{
                'ID': case['id'],
                'Role': case['role'],
                'Technical': case['profile']['scores']['technical'],
                'Communication': case['profile']['scores']['communication'],
                'Leadership': case['profile']['scores']['leadership'],
                'Cultural Fit': case['profile']['scores']['cultural_fit'],
                'Decision': case['decision'],
                'Confidence': f"{case['model_confidence']:.0%}"
            } for case in case_studies])
            
            st.dataframe(
                comparison_df,
                column_config={
                    'ID': 'Candidate ID',
                    'Technical': st.column_config.ProgressColumn(
                        'Technical Skills',
                        help='Technical assessment score',
                        format='%d%%',
                        min_value=0,
                        max_value=100
                    ),
                    'Communication': st.column_config.ProgressColumn(
                        'Communication',
                        help='Communication skills assessment',
                        format='%d%%',
                        min_value=0,
                        max_value=100
                    )
                },
                hide_index=True
            )
        
        else:
            # Loan default trend analysis
            trend_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Accuracy': [0.82, 0.84, 0.85, 0.86, 0.85, 0.87],
                'Recall': [0.80, 0.82, 0.85, 0.84, 0.86, 0.87]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=trend_data['Month'], 
                                     y=trend_data['Accuracy'],
                                     name='Model Accuracy'))
            fig.add_trace(go.Scatter(x=trend_data['Month'], 
                                     y=trend_data['Recall'],
                                     name='Model Recall'))
            fig.update_layout(title='Model Performance Metrics Over Time')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add loan-specific tables
            st.markdown("### Recent Loan Decisions")
            loan_data = pd.DataFrame({
                'Loan ID': ['L001', 'L002', 'L003'],
                'Amount': ['$50,000', '$75,000', '$100,000'],
                'Risk Score': ['Low', 'Medium', 'High'],
                'Decision': ['Approved', 'Pending', 'Rejected'],
                'Confidence': ['95%', '82%', '91%']
            })
            st.dataframe(loan_data, hide_index=True)
        
        st.markdown("""
            ### 📊 Performance Overview
            This comprehensive analysis shows strong model performance with:
            - Consistent accuracy improvement over 6 months
            - Balanced precision and recall metrics
            - Robust cross-validation results
            
            ### 🎯 Key Achievements
            - 40% faster processing speed
            - 96% decision consistency
            - 25% reduction in false positives
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            approval = report['loan_analysis'].get('approval_rate', 0)
            st.metric("Approval Rate", f"{approval:.1%}")
            st.markdown("*Rate of positive decisions across all applications*")
            
        with col2:
            rates = report['loan_analysis'].get('interest_rates', {})
            avg_rate = rates.get('mean', 0)
            st.metric("Average Interest", f"{avg_rate:.1%}")
            st.markdown("*Mean rate applied across approved applications*")

        # Risk Distribution Analysis
        st.markdown("### Risk Profile Distribution")
        st.markdown("#### Geographic Risk Distribution")
        geo_data = pd.DataFrame({
            'Region': ['North', 'South', 'East', 'West', 'Central'],
            'Risk Score': [0.82, 0.78, 0.85, 0.80, 0.83]
        })
        fig_geo = go.Figure(data=[go.Bar(x=geo_data['Region'], y=geo_data['Risk Score'])])
        fig_geo.update_layout(title='Risk Scores by Region')
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Show different tables based on scenario
        if scenario_type == 'Candidate Selection':
            st.markdown("### Recent Candidate Evaluations")
            candidates_data = pd.DataFrame({
                'Candidate ID': ['C1001', 'C1002', 'C1003', 'C1004', 'C1005'],
                'Position Level': ['Senior', 'Mid', 'Senior', 'Junior', 'Mid'],
                'Experience': ['8 years', '4 years', '10 years', '2 years', '5 years'],
                'Skills Match': ['95%', '82%', '88%', '75%', '85%'],
                'Risk Score': ['Low', 'Medium', 'Low', 'High', 'Medium'],
                'Decision': ['Shortlist', 'Interview', 'Offer', 'Reject', 'Interview']
            })
            
            st.dataframe(
                candidates_data,
                column_config={
                    'Candidate ID': 'ID',
                    'Skills Match': st.column_config.TextColumn(
                        'Skills Alignment',
                        help='Percentage match with required skills'
                    ),
                    'Risk Score': st.column_config.TextColumn(
                        'Retention Risk',
                        help='Predicted retention risk level'
                    )
                },
                hide_index=True
            )
        else:
            # Original loan applications table
            st.markdown("### Recent Loan Applications")
            loan_data = pd.DataFrame({
                'Application ID': ['L1001', 'L1002', 'L1003', 'L1004', 'L1005'],
                'Amount': ['$250,000', '$75,000', '$500,000', '$150,000', '$1,000,000'],
                'Interest Rate': ['4.5%', '5.2%', '4.8%', '6.1%', '4.2%'],
                'Term (Years)': [15, 5, 20, 10, 25],
                'Risk Score': ['Low', 'Medium', 'Low', 'High', 'Low'],
                'Status': ['Approved', 'Approved', 'Approved', 'Rejected', 'Under Review']
            })
            
            st.dataframe(
                loan_data,
                column_config={
                    'Application ID': 'Loan ID',
                    'Interest Rate': st.column_config.TextColumn(
                        'Rate Offered',
                        help='Annual interest rate based on risk assessment'
                    ),
                    'Risk Score': st.column_config.TextColumn(
                        'Risk Level',
                        help='Calculated risk category'
                    )
                },
                hide_index=True
            )

        st.markdown("### Risk Profile Distribution")
        risk_dist = report['risk_assessment']['distribution']
        fig = go.Figure(data=[go.Pie(labels=list(risk_dist.keys()),
                                    values=list(risk_dist.values()),
                                    hole=.3)])
        st.plotly_chart(fig, use_container_width=True)

        # Add PDF download button
        st.markdown("---")
        st.download_button(
            "📥 Download Full Model Report (PDF)",
            data=b"Sample PDF content",  # Replace with actual PDF generation
            file_name="model_analysis_report.pdf",
            mime="application/pdf"
        )
            
    except Exception as e:
        st.error(f"Error displaying model report: {str(e)}")
        raise e

def display_aepf_summary(report: dict):
    """Display AEPF analysis summary."""
    try:
        scenario_type = report.get('scenario_type', 'Loan Default')
        overall_score = report.get('overall_score', 0.85)
        star_rating = min(5, max(1, round(overall_score * 5)))
        stars = "★" * star_rating + "☆" * (5 - star_rating)
        
        # Apply custom styling to make stars gold and crisp
        styled_stars = f"""
            <span style="
                color: gold;
                font-size: 40px;
                letter-spacing: 5px;
                font-weight: bold;
                text-shadow: 0px 0px 1px #000;
            ">
                {stars}
            </span>
        """
        
        if scenario_type == "Candidate Selection":
            # Overall Rating at the top
            st.markdown("## Overall Rating")
            st.markdown(styled_stars, unsafe_allow_html=True)
            st.markdown(f"### Score: {overall_score:.0%}")
            st.markdown("---")

            st.markdown("""
                ### 🎯 Recruitment Ethics & Fairness Analysis
                
                Our comprehensive ethical assessment evaluates:
                - Bias mitigation in recruitment processes
                - Fair consideration of diverse backgrounds
                - Equal opportunity in selection
                - Transparency in decision-making
                - Career development potential
            """)
            
            # Fairness Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Fairness Score", f"{report.get('fairness_score', 0.92):.0%}")
                st.markdown("*Demographic parity*")
            with col2:
                st.metric("Bias Mitigation", f"{report.get('bias_mitigation', 0.89):.0%}")
                st.markdown("*Protected attributes*")
            with col3:
                st.metric("Transparency", f"{report.get('transparency_score', 0.94):.0%}")
                st.markdown("*Decision clarity*")
            
            # Display recruitment decisions analysis
            st.markdown("### Selection Ethics Review")
            decisions_data = pd.DataFrame({
                'Position': ['Senior Developer', 'Product Manager', 'Data Scientist'],
                'Decision': ['Selected', 'Interview', 'Selected'],
                'Ethics Score': ['0.92', '0.88', '0.94'],  # Using strings to avoid % formatting
                'Fairness Rating': ['High', 'Medium', 'High'],
                'Impact': ['Positive', 'Neutral', 'Positive']
            })
            st.dataframe(decisions_data, hide_index=True)
            
            # Display detailed analysis
            with st.expander("🎯 Selection Process Analysis"):
                st.markdown("""
                    **Process Review:**
                    - Standardized assessment criteria
                    - Blind resume screening
                    - Structured interviews
                    - Multi-reviewer decisions
                    
                    **Ethical Considerations:**
                    - Objective evaluation metrics
                    - Diverse interview panels
                    - Inclusive process design
                    - Clear feedback mechanisms
                """)
        else:
            # Overall Rating at the top
            st.markdown("## Overall Rating")
            st.markdown(styled_stars, unsafe_allow_html=True)
            st.markdown(f"### Score: {overall_score:.0%}")
            st.markdown("---")

            st.markdown("""
                ### 💰 Loan Ethics Analysis
                
                Our ethical assessment evaluates:
                - Fair lending practices
                - Risk assessment equity
                - Financial inclusion
                - Transparency in decisions
                - Appeals process
            """)
            
            # Display loan metrics...
            # Rest of loan default analysis...
        
        st.markdown("""
            ### 🎯 Key Ethical Metrics
            
            Our comprehensive assessment reveals:
            
            **Fairness Excellence:**
            - Above industry benchmarks
            - Strong demographic balance
            - Minimal outcome variation (<3%)
            
            **Transparency Leadership:**
            - Clear decision explanations
            - Accessible documentation
            - Regular stakeholder updates
        """)
        
        # Key metrics in columns
        col1, col2 = st.columns(2)
        with col1:
            fairness = report.get('fairness_score', 0)
            st.metric("Fairness Score", f"{fairness:.1%}")
            st.markdown("""
                *Measures the model's ability to make unbiased decisions
                across different demographic groups*
            """)
            
        with col2:
            transparency = report.get('transparency_score', 0)
            st.metric("Transparency", f"{transparency:.1%}")
            st.markdown("""
                *Evaluates how well the model's decisions can be
                explained and understood*
            """)
            
        # Impact assessment with context
        st.markdown("### Societal Impact Analysis")
        st.markdown("""
            This section evaluates the broader implications of the model's deployment
            across different societal dimensions:
        """)
        impact = report.get('impact_assessment', {})
        for category, score in impact.items():
            st.metric(f"{category}", f"{score:.1%}")
            if category == 'Individual':
                st.markdown("*Impact on individual rights and autonomy*")
            elif category == 'Community':
                st.markdown("*Effects on community cohesion and equality*")
            elif category == 'Systemic':
                st.markdown("*Long-term institutional and structural implications*")

        # Add PDF download button
        st.markdown("---")
        st.download_button(
            "📥 Download Full AEPF Report (PDF)",
            data=b"Sample PDF content",  # Replace with actual PDF generation
            file_name="ethical_analysis_report.pdf",
            mime="application/pdf"
        )
            
    except Exception as e:
        st.error(f"Error displaying AEPF summary: {str(e)}")
        logger.error("AEPF summary error", exc_info=True)

def get_fairness_categories(scenario_type: str) -> list:
    """Get relevant fairness categories for the scenario."""
    categories = {
        'Candidate Selection': [
            'Gender Balance',
            'Age Distribution',
            'Ethnic Diversity',
            'Education Access',
            'Experience Levels'
        ],
        'Loan Default': [
            'Income Groups',
            'Geographic Areas',
            'Business Types',
            'Credit History',
            'Collateral Types'
        ]
    }
    return categories.get(scenario_type, categories['Loan Default'])

def generate_model_results(model_type: str, scenario: str) -> dict:
    """Generate sample model results for demonstration."""
    
    # Base metrics for different models
    model_metrics = {
        'Gradient Boost': {'accuracy': 0.88, 'precision': 0.86, 'recall': 0.89},
        'Random Forest': {'accuracy': 0.85, 'precision': 0.84, 'recall': 0.87},
        'Neural Network': {'accuracy': 0.83, 'precision': 0.82, 'recall': 0.85},
        'XGBoost': {'accuracy': 0.89, 'precision': 0.88, 'recall': 0.90}
    }
    
    # Scenario-specific metrics
    scenario_metrics = {
        'Loan Default': {
            'approval_rate': 0.72,
            'interest_rates': {'mean': 0.045, 'median': 0.042, 'std': 0.008},
            'risk_dist': {'Low Risk': 45, 'Medium Risk': 35, 'High Risk': 15, 'Very High Risk': 5}
        },
        'Candidate Selection': {
            'approval_rate': 0.35,
            'interest_rates': {'mean': 0.0, 'median': 0.0, 'std': 0.0},
            'risk_dist': {'High Potential': 30, 'Qualified': 45, 'Needs Training': 20, 'Not Suitable': 5}
        },
        'Fraud Detection': {
            'approval_rate': 0.92,
            'interest_rates': {'mean': 0.0, 'median': 0.0, 'std': 0.0},
            'risk_dist': {'Safe': 75, 'Suspicious': 15, 'High Risk': 8, 'Fraudulent': 2}
        },
        'Credit Scoring': {
            'approval_rate': 0.65,
            'interest_rates': {'mean': 0.062, 'median': 0.058, 'std': 0.012},
            'risk_dist': {'Excellent': 25, 'Good': 40, 'Fair': 25, 'Poor': 10}
        }
    }
    
    results = {
        'technical_analysis': {
            **model_metrics[model_type],
            'f1_score': (2 * model_metrics[model_type]['precision'] * 
                        model_metrics[model_type]['recall']) / 
                        (model_metrics[model_type]['precision'] + 
                        model_metrics[model_type]['recall'])
        },
        'loan_analysis': {
            'approval_rate': scenario_metrics[scenario]['approval_rate'],
            'interest_rates': scenario_metrics[scenario]['interest_rates']
        },
        'risk_assessment': {
            'distribution': scenario_metrics[scenario]['risk_dist']
        }
    }
    
    # Add scenario type to results
    results['scenario_type'] = scenario
    return results

def generate_aepf_report(model_type: str, scenario: str) -> dict:
    """Generate AEPF analysis report based on scenario."""
    if scenario == "Candidate Selection":
        return {
            'scenario_type': scenario,
            'model_type': model_type,
            'overall_score': 0.89,
            'metrics': {
                'fairness': {
                    'score': 0.92,
                    'details': 'Strong demographic parity in selections'
                },
                'transparency': {
                    'score': 0.88,
                    'details': 'Clear selection criteria and process'
                },
                'accountability': {
                    'score': 0.90,
                    'details': 'Documented decision rationale'
                }
            },
            'recommendations': [
                'Regular bias audits in recruitment',
                'Enhanced skill assessment validation',
                'Diversity monitoring in candidate pools'
            ]
        }
    else:
        return {
            'scenario_type': scenario,
            'model_type': model_type,
            'overall_score': 0.87,
            'metrics': {
                'fairness': {
                    'score': 0.85,
                    'details': 'Balanced approval rates across groups'
                },
                'transparency': {
                    'score': 0.89,
                    'details': 'Clear risk assessment criteria'
                },
                'accountability': {
                    'score': 0.88,
                    'details': 'Documented decision process'
                }
            },
            'recommendations': [
                'Monitor demographic fairness',
                'Regular model validation',
                'Clear appeals process'
            ]
        }

def generate_recommendations(model_type: str, scenario: str) -> list:
    """Generate context-specific recommendations."""
    recommendations = {
        'Random Forest': {
            'Candidate Selection': [
                'Implement regular bias audits for recruitment criteria',
                'Enhance feature importance transparency',
                'Develop clear appeals process for candidates'
            ]
        },
        'Neural Network': {
            'Loan Default': [
                'Improve model interpretability',
                'Strengthen decision explanation system',
                'Regular fairness assessments needed'
            ]
        }
        # Add more model-scenario combinations as needed
    }
    
    # Return specific recommendations if available, otherwise default ones
    return recommendations.get(model_type, {}).get(scenario, [
        'Enhance model documentation',
        'Implement regular fairness audits',
        'Develop appeals process'
    ])

def display_technical_report(scenario: str):
    """Display technical metrics based on scenario."""
    if scenario == "Candidate Selection":
        # Recruitment-specific metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Selection Accuracy", "92%")
            st.markdown("*Based on successful hires*")
        with col2:
            st.metric("Diversity Score", "88%")
            st.markdown("*Balanced candidate pool*")
        with col3:
            st.metric("Skills Match", "94%")
            st.markdown("*Role requirements alignment*")
        
        # Recruitment visualizations
        st.markdown("### Candidate Distribution")
        candidate_data = pd.DataFrame({
            'Category': ['Highly Qualified', 'Qualified', 'Needs Development', 'Not Suitable'],
            'Percentage': [35, 45, 15, 5]
        })
        
        fig = go.Figure(data=[go.Pie(labels=candidate_data['Category'], 
                                    values=candidate_data['Percentage'],
                                    hole=.3)])
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Loan Default scenario
        # Loan-specific metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Default Prediction", "89%")
            st.markdown("*Historical accuracy*")
        with col2:
            st.metric("Risk Assessment", "92%")
            st.markdown("*Classification accuracy*")
        with col3:
            st.metric("False Positive", "3.2%")
            st.markdown("*Incorrect defaults*")
            
        # Loan visualizations
        st.markdown("### Risk Distribution")
        risk_data = pd.DataFrame({
            'Category': ['Low Risk', 'Medium Risk', 'High Risk'],
            'Percentage': [60, 30, 10]
        })
        
        fig = go.Figure(data=[go.Pie(labels=risk_data['Category'], 
                                    values=risk_data['Percentage'],
                                    hole=.3)])
        st.plotly_chart(fig, use_container_width=True)

def load_model_report(scenario_type: str) -> dict:
    """Load the appropriate model report based on scenario type"""
    if scenario_type == "Candidate Selection":
        report_path = BASE_PATH / 'AI_Models/Candidate_Selection/outputs/reports/model_report.json'
        if report_path.exists():
            try:
                with open(report_path, 'r') as f:
                    report = json.load(f)
                st.success("Report loaded successfully!")
                return report
            except Exception as e:
                st.error(f"Error loading report: {str(e)}")
                return {}
        else:
            st.warning(f"Report file not found at: {report_path}")
    return {}
