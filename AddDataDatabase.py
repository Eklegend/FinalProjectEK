import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/"
})

# This is the reference path of the database that will create a student directory that will have student id
ref = db.reference('Students')

data = {
    "121212":
        {
            "Name": "Hariharan Elangovan",
            "Major": "Informatics",
            "Enrolling_Year": "2020",
            "Total_attendence": 5,
            "Standing": "G",  # G for good
            "Year": 4,
            "Last_attendance_time": "2023-11-28 01:58:33"

        },
    "131313":
        {
            "Name": "Alexandra Daddario",
            "Major": "Data Finance",
            "Enrolling_Year": "2021",
            "Total_attendence": 5,
            "Standing": "G",  # G for good
            "Year": 5,
            "Last_attendance_time": "2023-11-11 01:58:33"

        },
    "141414":
        {
            "Name": "Tony Stark",
            "Major": "Computer Science",
            "Enrolling_Year": "2023",
            "Total_attendence": 0,
            "Standing": "B",  # G for good
            "Year": 1,
            "Last_attendance_time": "2023-1-1 11:58:33"

        }
}

# This is how we unzip json data dictionary in python
for key, value in data.items():
    ref.child(key).set(value)  # we use child if we want to send data to specific directory
