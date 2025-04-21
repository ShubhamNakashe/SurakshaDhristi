import streamlit as st
from utils.helpers import fetch_mobile_ip_locations, cctv_locations, find_nearest_mobile
from utils.sms import send_sms_alert
from ViolTry import detect_violence
from gender_detect import count_genders

def live_surveillance():
    st.title("📹 Live CCTV Surveillance Dashboard")

    fetch_mobile_ip_locations()

    video_files = [
        "Videos/V.mp4",     # Kurla
        "Videos/NonV2.mp4",  # Andheri
        # "Videos/V5.mp4",     # Bandra
        "Videos/NV9.mp4",    # Vashi
        "Videos/V9.mp4",     # Dadar
        "Videos/V6.MP4",     # Thane
        "Videos/V10.MP4"      # Borivali (repeated or replace with correct if needed)
    ]

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = [None] * len(video_files)

    for i in range(3):  # 3 rows
        cols = st.columns(3)
        for j in range(3):  # 3 videos per row
            idx = i * 3 + j
            if idx >= len(video_files):
                break

            location_data = cctv_locations[idx]
            location_name = location_data["location"]

            with cols[j]:
                st.video(video_files[idx])
                st.markdown(f"📍 Location: {location_name}")

                if st.button(f"Detect Gender & Violence", key=f"gender_{idx}"):
                    male_percent, female_percent = count_genders(video_files[idx])
                    st.write(f"👦 Male: {male_percent}% | 👧 Female: {female_percent}%")

                    if male_percent > female_percent:
                        st.warning("⚠️ More males than females. Checking for violence...")
                        st.session_state.analysis_results[idx] = detect_violence(video_files[idx])
                    else:
                        st.success("✅ No abnormal gender ratio. Skipping violence detection.")

                    result = st.session_state.analysis_results[idx]
                    if isinstance(result, str):
                        if "No Violence" in result:
                            st.success(result)
                        else:
                            st.error(result)
                    elif result is not None:
                        st.warning("⚠️ Unexpected result type from detect_violence()")

                # 🚨 Updated: Route specific locations to fixed number, rest use nearest
                if st.button(f"Send Alert ({location_name})", key=f"alert_{idx}"):
                    location_lower = location_name.lower()

                    # Only fixed route for Andheri, Vashi, Dadar
                    if any(loc in location_lower for loc in ["andheri", "vashi", "dadar"]):
                        contact_number = "+919321573202"
                        send_sms_alert(contact_number, f"🚨 Alert: Issue at {location_name} CCTV.")
                        st.success(f"📲 Alert sent to {contact_number} (Fixed Routing) for: {location_name}")
                    else:
                        # Nearest routing for others
                        nearest_number, nearest_ip, dist = find_nearest_mobile(location_data)
                        if nearest_number:
                            send_sms_alert(nearest_number, f"🚨 Alert: Issue at {location_name} CCTV. Nearest IP ({nearest_ip}) alerted.")
                            st.success(f"📲 Alert sent to nearest contact: {nearest_number} (Distance: {dist:.2f} km)")
                        else:
                            st.error("❌ Could not find nearest responder.")

live_surveillance()
