import streamlit as st
from utils.helpers import fetch_mobile_ip_locations, find_nearest_mobile, cctv_locations, tracked_ips
from utils.sms import send_sms_alert
from ViolTry import detect_violence
from gender_detect import count_genders  # NEW IMPORT

def live_surveillance():
    st.title("Live CCTV Surveillance")
    fetch_mobile_ip_locations()

    locations = ['Andheri', 'Bandra', 'Colaba', 'Dadar', 'Thane', 'Borivali']
    video_files = ["Videos/NonV.mp4", "Videos/NonV2.mp4", "Videos/NonV3.mp4", "Videos/NonV4.mp4", "Videos/NonV5.mp4", "Videos/fight2.MP4"]

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = [None] * len(video_files)

    for i in range(2):
        cols = st.columns(3)
        for j in range(3):
            idx = i * 3 + j
            with cols[j]:
                st.video(video_files[idx])
                st.write(f"Location: {locations[idx]}")

                # Run gender detection automatically
                if st.button(f"Detect Gender ({locations[idx]})", key=f"gender_{idx}"):
                    male_percent, female_percent = count_genders(video_files[idx])
                    st.write(f"👦 Male: {male_percent}% | 👧 Female: {female_percent}%")

                    if male_percent > female_percent:
                        st.write("🔍 More males than females. Running violence detection...")
                        st.session_state.analysis_results[idx] = detect_violence(video_files[idx])
                    else:
                        st.write("✅ Males not more than females. Skipping violence detection.")


                result = st.session_state.analysis_results[idx]
                if result:
                    st.success(result) if "No Violence" in result else st.error(result)

                if st.button(f"Send Alert ({locations[idx]})", key=f"alert_{idx}"):
                    nearest_mobile, nearest_ip, dist = find_nearest_mobile(cctv_locations[idx])
                    if nearest_mobile:
                        for t in tracked_ips:
                            if nearest_ip == t['ip']:
                                send_sms_alert(t['phone_number'], f"🚨 Nearest to {locations[idx]} CCTV")
                                break
                        else:
                            st.write(f"Alert sent to IP: {nearest_ip}")
                    else:
                        st.warning("No valid mobile location.")

live_surveillance()
