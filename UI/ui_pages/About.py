import streamlit as st

def show():
    """Show the about page content."""
    print("About.py show() function called")  # Debug print
    
    # Clear any previous elements
    st.empty()
    
    st.title("About AEPF")
    
    # Use a container to ensure content is only rendered once
    with st.container():
        st.markdown("""
        ## Adaptive Ethical Prism Framework (AEPF)

        The **Adaptive Ethical Prism Framework (AEPF)** is a pioneering ethical decision-making system designed to evaluate and enhance the transparency, accountability, and fairness of artificial intelligence (AI) systems. Developed by Leo M. Cole in 2024 in Harrogate, United Kingdom, AEPF provides a structured approach to assessing AI outputs across multiple ethical dimensions, ensuring their alignment with human values, societal well-being, and long-term sustainability.

        ### Overview
        AEPF operates as a modular framework, integrating various components to analyze and audit AI decision-making processes. Central to the framework is the **Ethical Governor**, which leverages a **Context Engine** and five distinct "prisms":

        1. **Human-Centric Prism**: Prioritizes individual rights and well-being.
        2. **Ecocentric Prism**: Focuses on environmental sustainability and ecological balance.
        3. **Sentient-First Prism**: Considers the ethical treatment of sentient beings, both human and non-human.
        4. **Innovation-Centric Prism**: Evaluates the impact of decisions on technological and creative progress.
        5. **Community-Centric Prism**: Advocates for the greater good and societal harmony.

        ### Key Features
        - **Ethical Scoring System**: A five-star grading system simplifies ethical evaluations for a broad audience.
        - **Transparency and Reporting**: AEPF supports four levels of reporting, from technical raw data to high-level summaries.
        - **Memory Component**: Enables the framework to retain and adapt based on past decisions.
        - **Modular Integration**: AEPF can audit or override existing AI systems.

        ### Applications
        AEPF has been applied in various domains, including:
        - **Healthcare**: Ensuring equitable treatment decisions.
        - **Finance**: Auditing AI models for loan default predictions.
        - **Human Resources**: Evaluating candidate selection processes.
        """)

        st.markdown("""
        ## Etho Shift

        **Etho Shift** is the organization behind the Adaptive Ethical Prism Framework (AEPF), dedicated to promoting ethical AI practices and fostering trust in autonomous decision-making systems. Founded by Leo M. Cole in 2024, Etho Shift operates on the principle of "Transparent Ethical Evolution."

        ### Mission
        Etho Shift's mission is to engender trust and transparency in AI decisions, ensuring the ethical deployment of both current and emerging technologies. The organization seeks to bridge the gap between technological innovation and societal values.

        ### Core Values
        1. **Transparency**: Open and accessible ethical evaluations.
        2. **Accountability**: Systems designed to be auditable and fair.
        3. **Sustainability**: Decisions that consider long-term impacts on society and the environment.

        ### Activities
        Etho Shift engages in:
        - **Framework Development**: Advancing AEPF to meet evolving ethical challenges.
        - **Education**: Simplifying AI ethics through resources like eBooks and workshops.
        - **Collaboration**: Partnering with organizations to embed ethical principles into AI systems.
        """)
        
        st.markdown("---")
        st.markdown("📧 info@etho-shift.com")

if __name__ == "__main__":
    print("About.py executed directly")  # Debug print
    show() 