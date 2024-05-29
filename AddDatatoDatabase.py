import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://final-year-project-nsec-default-rtdb.asia-southeast1.firebasedatabase.app"
})

ref = db.reference('Students')

data = {
    "2":
        {
            "name": "Sayantan Kar",
            "major": "Software Developer",
            "starting_year": 2020,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34",
            "last_attendance_date": "2023-11-11"
        },
    "3":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34",
            "last_attendance_date": "2023-11-11"
        },
    "4":
        {
            "name": "Debanjan Acharya",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34",
            "last_attendance_date": "2023-11-11"
        },
    "5":
        {
            "name": "Adway Dutta Gupta",
            "major": "Marketing",
            "starting_year": 2017,
            "total_attendance": 0,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-11-11 00:54:34",
            "last_attendance_date": "2023-11-11"
        },
    "1":
        {
            "name": "Akanksha Dey",
            "major": "Maths",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-11-11 00:54:34",
            "last_attendance_date": "2023-11-11"
        }
}

for key, value in data.items():
    ref.child(key).set(value)