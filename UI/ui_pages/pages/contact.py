import streamlit as st
import time
import random

def show():
    """Display the contact page content."""
    st.title("Contact Us")
    
    # Initialize session state for form submission
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    # Generate a unique form key using the current time and a random number
    form_key = f"contact_form_{int(time.time())}_{random.randint(0, 1000)}"
    
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
                    # Simulate sending an email
                    st.session_state.form_submitted = True
                    st.success("Thank you for your message! We will get back to you soon.")
                else:
                    st.error("Please fill in all required fields.")
    else:
        # Show reset button when form is submitted
        if st.button("Send Another Message"):
            st.session_state.form_submitted = False
            st.experimental_rerun()
    
    # Always show contact email at bottom
    st.markdown("---")
    st.markdown("📧 [info@etho-shift.com](mailto:info@etho-shift.com)")

if __name__ == "__main__":
    show()
