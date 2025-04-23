# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# from utils.helpers import fetch_mobile_ip_locations, cctv_locations
# import requests
# from geopy.distance import geodesic

# def ip_locator():
#     st.title("📍 CCTV Tracker ")
#     st.markdown("Each CCTV (🔴) is connected to its nearest mobile IP (🔵) using a single green line.")

#     tracked_mobiles = fetch_mobile_ip_locations()
#     plotted_ips = set()
#     mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)

#     # Step 1: Fetch mobile IP locations
#     ip_locations = {}
#     for mobile in tracked_mobiles:
#         ip = mobile["ip"]
#         lat, lon = None, None

#         try:
#             response = requests.get(f"http://ip-api.com/json/{ip}")
#             data = response.json()
#             lat, lon = data.get("lat"), data.get("lon")
#             if not lat or not lon:
#                 lat = mobile.get("latitude")
#                 lon = mobile.get("longitude")
#         except:
#             lat = mobile.get("latitude")
#             lon = mobile.get("longitude")

#         if lat and lon:
#             ip_locations[ip] = {
#                 "lat": lat,
#                 "lon": lon,
#                 "phone": mobile["phone_number"]
#             }

#     # Step 2: Plot mobile IPs (blue markers)
#     for ip, info in ip_locations.items():
#         mobile_coords = (info["lat"], info["lon"])
#         if ip not in plotted_ips:
#             folium.Marker(
#                 location=mobile_coords,
#                 popup=f"📱 Mobile IP: {ip}<br>📞 {info['phone']}",
#                 icon=folium.Icon(color='blue', icon='user', prefix='fa')
#             ).add_to(mumbai_map)
#             plotted_ips.add(ip)

#     # Step 3: Plot CCTV markers (red) and draw line to nearest mobile
#     for cctv in cctv_locations:
#         cctv_coords = (cctv['latitude'], cctv['longitude'])

#         folium.Marker(
#             location=cctv_coords,
#             popup=f"📷 CCTV: {cctv['location']}<br>📞 Alert: {cctv['phone_number']}",
#             icon=folium.Icon(color='red', icon='camera', prefix='fa')
#         ).add_to(mumbai_map)

#         # Find nearest mobile
#         nearest_ip = None
#         nearest_distance = float('inf')
#         nearest_coords = None

#         for ip, info in ip_locations.items():
#             mobile_coords = (info["lat"], info["lon"])
#             try:
#                 dist = geodesic(cctv_coords, mobile_coords).km
#                 if dist < nearest_distance:
#                     nearest_distance = dist
#                     nearest_ip = ip
#                     nearest_coords = mobile_coords
#             except:
#                 continue

#         if nearest_coords:
#             folium.PolyLine(
#                 locations=[cctv_coords, nearest_coords],
#                 color="green", weight=2, opacity=0.7
#             ).add_to(mumbai_map)

#     folium_static(mumbai_map)

# ip_locator()




# # import streamlit as st
# # import folium
# # from streamlit_folium import folium_static
# # from utils.helpers import fetch_mobile_ip_locations, cctv_locations, find_nearest_mobile

# # def ip_locator():
# #     st.title("📍 Live IP + CCTV Tracker with Heatmap")
# #     st.markdown("This map shows CCTV camera locations and their nearest tracked mobile device (based on IP geolocation).")

# #     # Initialize map centered around Mumbai
# #     mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)

# #     # Add CCTV locations
# #     for cctv in cctv_locations:
# #         folium.Marker(
# #             location=[cctv['latitude'], cctv['longitude']],
# #             popup=f"CCTV: {cctv['location']}<br>📞 Alert To: {cctv['phone_number']}",
# #             icon=folium.Icon(color='red', icon='camera', prefix='fa')
# #         ).add_to(mumbai_map)

# #         # Find nearest mobile IP to this CCTV
# #         nearest_phone, nearest_ip, distance = find_nearest_mobile(cctv)

# #         if nearest_phone and nearest_ip:
# #             try:
# #                 # Fetch IP location again to get lat/lon for line and marker
# #                 import requests
# #                 response = requests.get(f"http://ip-api.com/json/{nearest_ip}")
# #                 data = response.json()
# #                 mobile_lat, mobile_lon = data.get("lat"), data.get("lon")

# #                 # Mobile marker
# #                 folium.Marker(
# #                     location=[mobile_lat, mobile_lon],
# #                     popup=f"📱 Mobile IP: {nearest_ip}<br>📞: {nearest_phone}<br>Distance: {round(distance, 2)} km",
# #                     icon=folium.Icon(color='blue', icon='user', prefix='fa')
# #                 ).add_to(mumbai_map)

# #                 # Line between CCTV and mobile
# #                 folium.PolyLine(
# #                     locations=[
# #                         [cctv['latitude'], cctv['longitude']],
# #                         [mobile_lat, mobile_lon]
# #                     ],
# #                     color="green",
# #                     weight=2,
# #                     opacity=0.6
# #                 ).add_to(mumbai_map)

# #             except Exception as e:
# #                 st.error(f"❌ Could not locate IP {nearest_ip}: {e}")

# #     # Show map
# #     folium_static(mumbai_map)

# # ip_locator()

import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.helpers import fetch_mobile_ip_locations, cctv_locations
import requests
from geopy.distance import geodesic

# Set page configuration
st.set_page_config(page_title="CCTV Tracker - Suraksha Drishti", layout="wide")

# Custom CSS to match the screenshot
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #3b2a77 100%);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-top: 50px;
        color: white;
    }
    p {
        text-align: center;
        color: #d3d3d3;
        font-size: 16px;
    }
    /* Navigation bar styling */
    .nav-bar {
        display: flex;
        justify-content: flex-end;
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .nav-item {
        margin: 0 15px;
        font-size: 16px;
        color: white;
        text-decoration: none;
    }
    .nav-item:hover {
        color: #ff4d94;
    }
    /* Logo styling */
    .logo {
        height: 50px;
        margin-top: 10px;
    }
    /* Map container */
    .map-container {
        width: 100%;
        height: 600px; /* Adjust height as needed */
    }
    /* Zoom buttons styling */
    .zoom-buttons {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 5px;
    }
    .zoom-button {
        background-color: white;
        color: black;
        border: none;
        font-size: 20px;
        padding: 5px 10px;
        margin: 5px 0;
        cursor: pointer;
        border-radius: 5px;
    }
    .zoom-button:hover {
        background-color: #d3d3d3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo and Navigation Bar
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://via.placeholder.com/150x50?text=Suraksha+Drishti", width=150, clamp=True)  # Replace with your logo URL
with col2:
    st.markdown(
        """
        <div class="nav-bar">
            <a class="nav-item" href="http://localhost:8501/app.py">Home</a>
            <a class="nav-item" href="http://localhost:8501/pages/Crime_Dashboard.py">Dashboard</a>
            <a class="nav-item" href="http://localhost:8501/pages/CCTV_Tracker.py">CCTV</a>
            <a class="nav-item" href="http://localhost:8501/app.py">Live</a>
            <a class="nav-item" href="http://localhost:8501/app.py">Violence</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main Title and Description
st.markdown("<h1>📍 CCTV Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p>Each CCTV (🔴) is connected to its nearest mobile IP (🔵) using a green line.</p>", unsafe_allow_html=True)

# Create a two-column layout: narrow left for zoom buttons, wide right for map
col_left, col_right = st.columns([1, 10])

# Zoom buttons on the left
with col_left:
    st.markdown("<div class='zoom-buttons'>", unsafe_allow_html=True)
    st.markdown("<button class='zoom-button'>+</button>", unsafe_allow_html=True)
    st.markdown("<button class='zoom-button'>-</button>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Map on the right
with col_right:
    def ip_locator():
        tracked_mobiles = fetch_mobile_ip_locations()
        plotted_ips = set()
        mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)

        # Step 1: Fetch mobile IP locations
        ip_locations = {}
        for mobile in tracked_mobiles:
            ip = mobile["ip"]
            lat, lon = None, None

            try:
                response = requests.get(f"http://ip-api.com/json/{ip}")
                data = response.json()
                lat, lon = data.get("lat"), data.get("lon")
                if not lat or not lon:
                    lat = mobile.get("latitude")
                    lon = mobile.get("longitude")
            except:
                lat = mobile.get("latitude")
                lon = mobile.get("longitude")

            if lat and lon:
                ip_locations[ip] = {
                    "lat": lat,
                    "lon": lon,
                    "phone": mobile["phone_number"]
                }

        # Step 2: Plot mobile IPs (blue markers)
        for ip, info in ip_locations.items():
            mobile_coords = (info["lat"], info["lon"])
            if ip not in plotted_ips:
                folium.Marker(
                    location=mobile_coords,
                    popup=f"📱 Mobile IP: {ip}<br>📞 {info['phone']}",
                    icon=folium.Icon(color='blue', icon='user', prefix='fa')
                ).add_to(mumbai_map)
                plotted_ips.add(ip)

        # Step 3: Plot CCTV markers (red) and draw line to nearest mobile
        for cctv in cctv_locations:
            cctv_coords = (cctv['latitude'], cctv['longitude'])

            folium.Marker(
                location=cctv_coords,
                popup=f"📷 CCTV: {cctv['location']}<br>📞 Alert: {cctv['phone_number']}",
                icon=folium.Icon(color='red', icon='camera', prefix='fa')
            ).add_to(mumbai_map)

            # Find nearest mobile
            nearest_ip = None
            nearest_distance = float('inf')
            nearest_coords = None

            for ip, info in ip_locations.items():
                mobile_coords = (info["lat"], info["lon"])
                try:
                    dist = geodesic(cctv_coords, mobile_coords).km
                    if dist < nearest_distance:
                        nearest_distance = dist
                        nearest_ip = ip
                        nearest_coords = mobile_coords
                except:
                    continue

            if nearest_coords:
                folium.PolyLine(
                    locations=[cctv_coords, nearest_coords],
                    color="green", weight=2, opacity=0.7
                ).add_to(mumbai_map)

        folium_static(mumbai_map, width=1200, height=600)  # Adjust width to fill the column

    ip_locator()