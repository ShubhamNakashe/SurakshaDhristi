import streamlit as st

def send_sms_alert(phone, message):
    st.write(f"📨 SMS to {phone}: {message}")
    # Integrate Twilio API here if needed
