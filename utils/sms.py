from twilio.rest import Client
import streamlit as st

# ✅ Replace these with your actual Twilio credentials
TWILIO_ACCOUNT_SID = "ACb822d5b0106006cd503d710c3e0162a5"
TWILIO_AUTH_TOKEN = " 596db2fe0db69a61901a210607f3c92a"
TWILIO_PHONE_NUMBER = "+14246226918"  # Your Twilio phone number

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

