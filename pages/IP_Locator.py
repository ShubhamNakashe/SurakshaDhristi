import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.helpers import fetch_mobile_ip_locations, mobile_locations, crime_data

def ip_locator():
    st.title("Live IP Tracker + Heatmap")

    fetch_mobile_ip_locations()
    mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    for _, row in crime_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['crime_count'] / 2,
            color='red',
            fill=True,
            fill_opacity=0.6
        ).add_to(mumbai_map)

    for lat, lon, ip in mobile_locations:
        if lat and lon:
            folium.Marker(location=[lat, lon], popup=f"IP: {ip}", icon=folium.Icon(color='blue')).add_to(mumbai_map)

    folium_static(mumbai_map)

ip_locator()
