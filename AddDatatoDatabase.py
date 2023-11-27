import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://final-year-project-nsec-default-rtdb.asia-southeast1.firebasedatabase.app"
})

ref = db.reference('Students')

data = {
    "20":
        {
            "name": "Sayantan Kar",
            "major": "Robotics",
            "starting_year": 2020,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34"
        },
    "22":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)