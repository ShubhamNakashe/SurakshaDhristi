from twilio.rest import Client
import streamlit as st

# ✅ Replace these with your actual Twilio credentials
TWILIO_ACCOUNT_SID = "ACe501f1b54e736b18947e15c98c33ec7a"
TWILIO_AUTH_TOKEN = "98f333d82b9192fa7a6c7d09349a71fd"
TWILIO_PHONE_NUMBER = "+14704658812"  # Your Twilio phone number

my_phone_number=['+918850469020','+919321573202','+918104027851','+917756949603']

def send_sms_alert(phone, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        st.success(f"📨 SMS sent to {phone} (SID: {message.sid})")
    except Exception as e:
        st.error(f"❌ Failed to send SMS to {phone}: {e}")

