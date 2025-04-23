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
        color: #f8fafc;
        margin-bottom: 40px;
    }
    .nav-bar {
        display: flex;
        justify-content: flex-end;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .nav-item {
        margin: 0 15px;
        font-size: 16px;
        color: #e0e7ff;
        text-decoration: none;
    }
    .nav-item:hover {
        color: #f9a8d4;
    }
    .video-card {
        background-color: rgba(255, 255, 255, 0.06);
        border-radius: 15px;
        padding: 12px;
        margin: 10px;
        text-align: center;
        color: #e0e7ff;
    }
    .location-marker {
        color: #c084fc;
        font-size: 18px;
        margin-top: 8px;
        font-weight: bold;
    }
    .stButton>button {
        margin: 6px;
        padding: 8px 16px;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        
    }
    .stButton>button:nth-child(1) {
        background-color: #9333ea;
        color: white;
    }
    .stButton>button:nth-child(1):hover {
        background-color: #c084fc;
        color: #1e1b4b;
    }
    .stButton>button:nth-child(2) {
        background-color: #ef4444;
        color: white;
    }
    .stButton>button:nth-child(2):hover {
        background-color: #f87171;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Logo and Navigation Bar
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://via.placeholder.com/150x50?text=Suraksha+Drishti", width=150, clamp=True)
with col2:
    st.markdown(
        """
        <div class="nav-bar">
            <a class="nav-item" href="http://localhost:8501/app.py">Home</a>
            <a class="nav-item" href="http://localhost:8501/pages/Crime_Dashboard.py">Dashboard</a>
            <a class="nav-item" href="http://localhost:8501/pages/CCTV_Tracker.py">CCTV</a>
            <a class="nav-item" href="http://localhost:8501/pages/Live_Surveillance.py">Live</a>
            <a class="nav-item" href="http://localhost:8501/app.py">Violence</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main Title
st.markdown("<h1>📹 Live CCTV Surveillance Dashboard</h1>", unsafe_allow_html=True)

def live_surveillance():
    fetch_mobile_ip_locations()

    video_files = [
        "Videos/V.mp4",     # Kurla
        "Videos/NonV2.mp4",  # Andheri
        "Videos/NonV4.mp4",  # Vashi
        "Videos/V7.mp4",     # Dadar
        "Videos/V6.MP4",     # Thane
        "Videos/V5.MP4"      # Borivali
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

                if st.button(f"Send Alert ({location_name})", key=f"alert_{idx}",use_container_width=True):
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
