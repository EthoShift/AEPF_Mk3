import streamlit as st

def show():
    """Display the contact page content."""
    st.title("Contact Us")

    # Initialize session state for form submission
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    form_key = "contact_form_main"  # ✅ Fixed, consistent key

    # Display form if not submitted
    if not st.session_state.form_submitted:
        with st.form(form_key):
            # Contact details
            name = st.text_input("Name*")
            email = st.text_input("Email*")
            message = st.text_area("Message*")

            # Submit button
            submitted = st.form_submit_button("Submit")

            if submitted:
                if name and email and message:
                    st.session_state.form_submitted = True
                    st.success("Thank you for your message! We will get back to you soon.")
                else:
                    st.error("Please fill in all required fields.")
    else:
        if st.button("Send Another Message"):
            st.session_state.form_submitted = False
            st.experimental_rerun()

    st.markdown("---")
    st.markdown("📧 [info@etho-shift.com](mailto:info@etho-shift.com)")
