import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.helpers import fetch_mobile_ip_locations, cctv_locations
import requests
from geopy.distance import geodesic

def ip_locator():
    st.title("📍 CCTV Tracker ")
    st.markdown("Each CCTV (🔴) is connected to its nearest mobile IP (🔵) using a single green line.")

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

    folium_static(mumbai_map)

ip_locator()




# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# from utils.helpers import fetch_mobile_ip_locations, cctv_locations, find_nearest_mobile

# def ip_locator():
#     st.title("📍 Live IP + CCTV Tracker with Heatmap")
#     st.markdown("This map shows CCTV camera locations and their nearest tracked mobile device (based on IP geolocation).")

#     # Initialize map centered around Mumbai
#     mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=11)

#     # Add CCTV locations
#     for cctv in cctv_locations:
#         folium.Marker(
#             location=[cctv['latitude'], cctv['longitude']],
#             popup=f"CCTV: {cctv['location']}<br>📞 Alert To: {cctv['phone_number']}",
#             icon=folium.Icon(color='red', icon='camera', prefix='fa')
#         ).add_to(mumbai_map)

#         # Find nearest mobile IP to this CCTV
#         nearest_phone, nearest_ip, distance = find_nearest_mobile(cctv)

#         if nearest_phone and nearest_ip:
#             try:
#                 # Fetch IP location again to get lat/lon for line and marker
#                 import requests
#                 response = requests.get(f"http://ip-api.com/json/{nearest_ip}")
#                 data = response.json()
#                 mobile_lat, mobile_lon = data.get("lat"), data.get("lon")

#                 # Mobile marker
#                 folium.Marker(
#                     location=[mobile_lat, mobile_lon],
#                     popup=f"📱 Mobile IP: {nearest_ip}<br>📞: {nearest_phone}<br>Distance: {round(distance, 2)} km",
#                     icon=folium.Icon(color='blue', icon='user', prefix='fa')
#                 ).add_to(mumbai_map)

#                 # Line between CCTV and mobile
#                 folium.PolyLine(
#                     locations=[
#                         [cctv['latitude'], cctv['longitude']],
#                         [mobile_lat, mobile_lon]
#                     ],
#                     color="green",
#                     weight=2,
#                     opacity=0.6
#                 ).add_to(mumbai_map)

#             except Exception as e:
#                 st.error(f"❌ Could not locate IP {nearest_ip}: {e}")

#     # Show map
#     folium_static(mumbai_map)

# ip_locator()
