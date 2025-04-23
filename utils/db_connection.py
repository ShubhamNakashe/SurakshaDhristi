import firebase_admin
from firebase_admin import db, credentials

# ✅ Only initialize app if it's not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("utils\credentials.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://surakshadrishti-c9f5e-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

def save_crime_data(data):
    try:
        ref = db.reference("crime_reports")
        ref.push(data)
        print("✅ Data saved to Firebase!")
    except Exception as e:
        print("❌ Error saving to Firebase:", e)

def fetch_crime_data():
    ref = db.reference("crime_reports")
    data = ref.get()
    if data:
        return list(data.values())  # returns list of dicts
    else:
        return []


# Make db available for import
__all__ = ['save_crime_data', 'db','fetch_crime_data']
