# import streamlit as st
# from utils.helpers import fetch_mobile_ip_locations, cctv_locations, find_nearest_mobile
# from utils.sms import send_sms_alert
# from ViolTry import detect_violence
# from gender_detect import count_genders

# def live_surveillance():
#     st.title("📹 Live CCTV Surveillance Dashboard")

#     fetch_mobile_ip_locations()

#     video_files = [
#         "Videos/V.mp4",     # Kurla
#         "Videos/NonV2.mp4",  # Andheri
#         # "Videos/V5.mp4",     # Bandra
#         "Videos/NonV4.mp4",    # Vashi
#         "Videos/V7.mp4",     # Dadar
#         "Videos/V6.MP4",     # Thane
#         "Videos/V5.MP4"      # Borivali (repeated or replace with correct if needed)
#     ]

#     if "analysis_results" not in st.session_state:
#         st.session_state.analysis_results = [None] * len(video_files)

#     for i in range(3):  # 3 rows
#         cols = st.columns(3)
#         for j in range(3):  # 3 videos per row
#             idx = i * 3 + j
#             if idx >= len(video_files):
#                 break

#             location_data = cctv_locations[idx]
#             location_name = location_data["location"]

#             with cols[j]:
#                 st.video(video_files[idx])
#                 st.markdown(f"📍 Location: {location_name}")

#                 if st.button(f"Detect Gender & Violence", key=f"gender_{idx}"):
#                     male_percent, female_percent = count_genders(video_files[idx])
#                     st.write(f"👦 Male: {male_percent}% | 👧 Female: {female_percent}%")

#                     if male_percent > female_percent:
#                         st.warning("⚠️ More males than females. Checking for violence...")
#                         result = detect_violence(video_files[idx])
#                         st.session_state.analysis_results[idx] = result

#                         if isinstance(result, str):
#                             if "No Violence" in result:
#                                 st.success(result)
#                             else:
#                                 st.error(result)

#                                 # ✅ Automatically send alert here
#                                 location_lower = location_name.lower()
#                                 if any(loc in location_lower for loc in ["andheri", "vashi", "dadar"]):
#                                     contact_number = "+919321573202"
#                                     send_sms_alert(contact_number, f"🚨 Alert: Issue at {location_name} CCTV.")
#                                     st.success(f"📲 Alert sent to {contact_number} (Fixed Routing) for: {location_name}")
#                                 else:
#                                     nearest_number, nearest_ip, dist = find_nearest_mobile(location_data)
#                                     if nearest_number:
#                                         send_sms_alert(nearest_number, f"🚨 Alert: Issue at {location_name} CCTV. Nearest IP ({nearest_ip}) alerted.")
#                                         st.success(f"📲 Alert sent to nearest contact: {nearest_number} (Distance: {dist:.2f} km)")
#                                     else:
#                                         st.error("❌ Could not find nearest responder.")
#                         else:
#                             st.warning("⚠️ Unexpected result type from detect_violence()")
#                     else:
#                         st.success("✅ No abnormal gender ratio. Skipping violence detection.")

#                 # 🚨 Updated: Route specific locations to fixed number, rest use nearest
#                 if st.button(f"Send Alert ({location_name})", key=f"alert_{idx}"):
#                     location_lower = location_name.lower()

#                     # Only fixed route for Andheri, Vashi, Dadar
#                     if any(loc in location_lower for loc in ["andheri", "vashi", "dadar"]):
#                         contact_number = "+919321573202"
#                         send_sms_alert(contact_number, f"🚨 Alert: Issue at {location_name} CCTV.")
#                         st.success(f"📲 Alert sent to {contact_number} (Fixed Routing) for: {location_name}")
#                     else:
#                         # Nearest routing for others
#                         nearest_number, nearest_ip, dist = find_nearest_mobile(location_data)
#                         if nearest_number:
#                             send_sms_alert(nearest_number, f"🚨 Alert: Issue at {location_name} CCTV. Nearest IP ({nearest_ip}) alerted.")
#                             st.success(f"📲 Alert sent to nearest contact: {nearest_number} (Distance: {dist:.2f} km)")
#                         else:
#                             st.error("❌ Could not find nearest responder.")

# live_surveillance()

import streamlit as st
from utils.helpers import fetch_mobile_ip_locations, cctv_locations, find_nearest_mobile
from utils.sms import send_sms_alert
from ViolTry import detect_violence
from gender_detect import count_genders
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(page_title="Live CCTV Surveillance Dashboard - Suraksha Drishti", layout="wide")

# Custom CSS for enhanced color contrast and style
# Custom CSS for purple-themed dashboard
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #3b0a75 0%, #1e1b4b 100%);
        color: #f9fafb;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        font-size: 46px;
        font-weight: bold;
        text-align: center;
       color: #ffffff;  /* Changed to pure white */
        margin-bottom: 40px;
    }
    .nav-bar {
    display: flex;
    justify-content: flex-end;
    padding: 12px 20px;
    background: transparent;
    margin-bottom: 25px;
}

.nav-item {
    margin: 0 20px;
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
    transition: color 0.3s ease-in-out;
}

.nav-item:hover {
    color: #f9a8d4;
    text-decoration: underline;
}
.stButton>button {
    margin: 6px;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 900;  /* Bold text */
    font-size: 22px;   /* Larger font size */
    border: none;
    background-color: rgba(255, 255, 255, 0.1); /* Subtle hover effect */
    color: #f9a8d4;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    text-decoration: underline;
    background-color: rgba(255, 255, 255, 0.1); /* Subtle hover effect */
    color: #f9a8d4;
}
    .video-card {
        background-color: rgba(255, 255, 255, 0.06);
        border-radius: 15px;
        padding: 12px;
        margin: 10px;
        text-align: center;
        color: #ffffff;  /* Changed to pure white */
    }
    .location-marker {
        color: #ffffff;  /* Changed to pure white */
        font-size: 20px;
        margin-top: 10px;
        font-weight: 700;  /* bold */
        letter-spacing: 0.5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# # Logo and Navigation Bar
import streamlit as st

# Logo and Navigation Bar
col1, col2 = st.columns([1, 4])
with col1:
    st.image("Videos/logo3.png", width=150)

with col2:
    col2_1, col2_2, col2_3, col2_4, col2_5 = st.columns(5)
    with col2_1:
        if st.button("Home"):
            switch_page("app")  # if app.py is your main file
    with col2_2:
        if st.button("Locate on Map"):
            switch_page("ip locator")
    with col2_3:
        if st.button("CCTV Footage"):
            switch_page("live surveillance")
    with col2_4:
        if st.button("Live Cameras"):
            switch_page("WebCam")
    with col2_5:
        if st.button("Dashboard"):
            switch_page("crime dashboard")



# Main Title
st.markdown("<h1>📹 Live CCTV Surveillance Dashboard</h1>", unsafe_allow_html=True)

def live_surveillance():
    fetch_mobile_ip_locations()

    video_files = [
        "Videos/V.mp4",     # Kurla
        "Videos/V5.mp4",  # Andheri
        "Videos/NV7.mp4",  # Vashi
        "Videos/V7.mp4",     # Dadar
        "Videos/V10.MP4",     # Thane
        "Videos/NonV2.MP4"      # Borivali
    ]
    locations = ["Kurla", "Andheri", "Vashi", "Dadar", "Thane", "Borivali"]

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = [None] * len(video_files)

    for i in range(2):
        cols = st.columns(3)
        for j in range(3):
            idx = i * 3 + j
            if idx >= len(video_files):
                break

            location_data = cctv_locations[idx]
            location_name = locations[idx]

            with cols[j]:
                st.markdown("<div class='video-card'>", unsafe_allow_html=True)
                st.video(video_files[idx])
                st.markdown(f"<div class='location-marker'>📍 {location_name}</div>", unsafe_allow_html=True)

                if st.button(f"Detect Gender/Violence", key=f"gender_{idx}",use_container_width=True):
                    male_percent, female_percent = count_genders(video_files[idx])
                    st.write(f"👦 **Male:** {male_percent}% | 👧 **Female:** {female_percent}%")

                    if male_percent > female_percent:
                        st.warning("⚠️ **More males detected. Checking for violence...**")
                        result = detect_violence(video_files[idx])
                        st.session_state.analysis_results[idx] = result

                        if isinstance(result, str):
                            if "No Violence" in result:
                                st.success(f"✅ {result}")
                            else:
                                st.error(f"🚨 {result}")
                                location_lower = location_name.lower()
                                if any(loc in location_lower for loc in ["andheri", "vashi", "dadar"]):
                                    contact_number = "+919321573202"
                                    send_sms_alert(contact_number, f"🚨 Alert: Issue at {location_name} CCTV.")
                                    st.success(f"📲 Alert sent to **{contact_number}** (Fixed Routing)")
                                else:
                                    nearest_number, nearest_ip, dist = find_nearest_mobile(location_data)
                                    if nearest_number:
                                        send_sms_alert(nearest_number, f"🚨 Alert at {location_name}. Nearest IP ({nearest_ip}) alerted.")
                                        st.success(f"📲 Alert sent to **{nearest_number}** (Distance: {dist:.2f} km)")
                                    else:
                                        st.error("❌ Could not find nearest responder.")
                        else:
                            st.warning("⚠️ Unexpected response from `detect_violence()`.")
                    else:
                        st.success("✅ **No gender anomaly. Skipping violence detection.**")

                if st.button(f"Send Alert manually", key=f"alert_{idx}",use_container_width=True):
                    location_lower = location_name.lower()
                    if any(loc in location_lower for loc in ["andheri", "vashi", "dadar"]):
                        contact_number = "+919321573202"
                        send_sms_alert(contact_number, f"🚨 Alert: Issue at {location_name} CCTV.")
                        st.success(f"📲 Alert sent to **{contact_number}** (Fixed Routing)")
                    else:
                        nearest_number, nearest_ip, dist = find_nearest_mobile(location_data)
                        if nearest_number:
                            send_sms_alert(nearest_number, f"🚨 Alert at {location_name}. Nearest IP ({nearest_ip}) alerted.")
                            st.success(f"📲 Alert sent to **{nearest_number}** (Distance: {dist:.2f} km)")
                        else:
                            st.error("❌ Could not find nearest responder.")

                st.markdown("</div>", unsafe_allow_html=True)

live_surveillance()
