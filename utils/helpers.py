import requests
import geopy.distance
import pandas as pd

tracked_ips = [{'ip': '2409:4040:d8b:c943::d6c8:8d0b', 'phone_number': '+91 8850469020'},
               {'ip': '219.100.37.243', 'phone_number': '+91 7756949603'}]

police_gps = [(19.0760, 72.8777), (19.2183, 72.9781), (19.0204, 72.8479), (19.0350, 72.8595)]
cctv_locations = [(19.0760, 72.8777), (19.1200, 72.8800), (19.0840, 72.8850), (19.0450, 72.8870), (19.1600, 72.9180), (19.2000, 72.9550)]
crime_data = pd.DataFrame({'latitude': [19.0760, 19.2183, 19.0204],
                           'longitude': [72.8777, 72.9781, 72.8479],
                           'crime_count': [20, 35, 15]})

mobile_ips = ['8.8.8.8', '1.1.1.1'] + [ip['ip'] for ip in tracked_ips]
mobile_locations = []

def fetch_mobile_ip_locations():
    global mobile_locations
    mobile_locations = []
    for ip in mobile_ips:
        try:
            res = requests.get(f"https://ipapi.co/{ip}/json/")
            data = res.json()
            mobile_locations.append((data.get('latitude'), data.get('longitude'), ip))
        except:
            mobile_locations.append((None, None, ip))

def find_nearest_mobile(cctv_loc):
    min_dist = float('inf')
    nearest = None
    nearest_ip = None
    for lat, lon, ip in mobile_locations:
        if lat and lon:
            dist = geopy.distance.distance(cctv_loc, (lat, lon)).km
            if dist < min_dist:
                min_dist = dist
                nearest = (lat, lon)
                nearest_ip = ip
    return nearest, nearest_ip, min_dist
