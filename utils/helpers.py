# helpers.py

import requests
import geopy.distance

tracked_ips = [
    # {'ip': '2409:4040:d8b:c943::d6c8:8d0b', 'phone_number': '+918850469020'},
    {'ip': '103.148.62.181', 'phone_number': '+918850469020'},
    {'ip': '192.168.0.240', 'phone_number': '+919321573202', 'latitude': 19.0760, 'longitude': 72.8774},
    # {'ip': '2409:40c0:2007:acc:4132:9458:4a3a:efef', 'phone_number': '+919321573202'},  # Bandra
    # {'ip': '2409:40c0:2007:acc:4132:9458:4a3a:efef', 'phone_number': '+919321573202', 'latitude': 19.0600, 'longitude': 72.8365},
    {'ip': '2409:40c0:103d:5003:e52b:af5d:c9b6:ec6d', 'phone_number': '+917756949603'},  # Dadar
]

# helpers.py

# cctv_locations = [
#     {'location': 'Kurla',    'latitude': 19.0700, 'longitude': 72.8826,},
#     {'location': 'Bandra',   'latitude': 19.0600, 'longitude': 72.8365},
#     {'location': 'Colaba',   'latitude': 18.9100, 'longitude': 72.8090},
#     {'location': 'Dadar',    'latitude': 19.0178, 'longitude': 72.8446},
#     {'location': 'Thane',    'latitude': 19.2183, 'longitude': 72.9781},
#     {'location': 'Borivali', 'latitude': 19.2288, 'longitude': 72.8541},
# ]


cctv_locations = [
    {'location': 'Kurla',    'latitude': 19.0700, 'longitude': 72.8826, 'phone_number': '+917756949603'}, 
    {'location': 'Andheri',  'latitude': 19.1197, 'longitude': 72.8468, 'phone_number': '+919321573202'},
    # {'location': 'Bandra',   'latitude': 19.0600, 'longitude': 72.8365, 'phone_number': '+919321573202'},
    {'location': 'Vashi',   'latitude': 19.0759, 'longitude': 72.8771, 'phone_number': '+919321573202'},
    {'location': 'Dadar',    'latitude': 19.0184, 'longitude': 72.8446, 'phone_number': '+919321573202'},
    {'location': 'Thane',    'latitude': 19.2183, 'longitude': 72.9781, 'phone_number': '+918850469020'},
    {'location': 'Borivali', 'latitude': 19.2288, 'longitude': 72.8541, 'phone_number': '+918850469020'},
]
def fetch_mobile_ip_locations():
    print("📡 Fetching mobile IP locations (simulated)...")
    return tracked_ips

def get_phone_by_ip(ip):
    for device in tracked_ips:
        if device['ip'] == ip:
            return device['phone_number']
    return None

def find_nearest_mobile(cctv_location):
    cctv_lat = cctv_location['latitude']
    cctv_lon = cctv_location['longitude']
    nearest_mobile = None
    nearest_ip = None
    min_distance = float('inf')

    for mobile in tracked_ips:
        try:
            response = requests.get(f"http://ip-api.com/json/{mobile['ip']}")
            data = response.json()
            lat, lon = data.get("lat"), data.get("lon")

            if lat and lon:
                distance = geopy.distance.geodesic((cctv_lat, cctv_lon), (lat, lon)).km
                if distance < min_distance:
                    min_distance = distance
                    nearest_ip = mobile["ip"]
                    nearest_mobile = mobile["phone_number"]
        except Exception as e:
            print(f"Error fetching location for {mobile['ip']}: {e}")

    return nearest_mobile, nearest_ip, min_distance
