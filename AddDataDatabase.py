import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from course_selector import choose_course

cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/"
})

# This is the reference path of the database that will create a student directory that will have student id
ref = db.reference('Courses')

data = {
    "121212":
        {
            "Name": "Hariharan Elangovan",
            "Major": "Informatics",
            "Enrolling_Year": "2020",
            "Total_attendance": 0,
            "Standing": 4.6,  # G for good
            "Year": 4,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "131313":
        {
            "Name": "Alexandra Daddario",
            "Major": "Data Finance",
            "Enrolling_Year": "2021",
            "Total_attendance": 0,
            "Standing": 5.0,  # G for good
            "Year": 5,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "141414":
        {
            "Name": "Tony Stark",
            "Major": "Computer Science",
            "Enrolling_Year": "2023",
            "Total_attendance": 0,
            "Standing": 3.0,  # G for good
            "Year": 1,
            "Last_attendance_time": "2023-01-01 01:01:01"

        }
}

data2 = {
    "121212":
        {
            "Name": "Hariharan Elangovan",
            "Major": "Informatics",
            "Enrolling_Year": "2020",
            "Total_attendance": 0,
            "Standing": 4.6,  # G for good
            "Year": 4,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "131313":
        {
            "Name": "Alexandra Daddario",
            "Major": "Data Finance",
            "Enrolling_Year": "2021",
            "Total_attendance": 0,
            "Standing": 5.0,  # G for good
            "Year": 5,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "141414":
        {
            "Name": "Tony Stark",
            "Major": "Computer Science",
            "Enrolling_Year": "2023",
            "Total_attendance": 0,
            "Standing": 3.0,  # G for good
            "Year": 1,
            "Last_attendance_time": "2023-01-01 01:01:01"

        }



}

data3 = {
    "121212":
        {
            "Name": "Hariharan Elangovan",
            "Major": "Informatics",
            "Enrolling_Year": "2020",
            "Total_attendance": 0,
            "Standing": 4.6,  # G for good
            "Year": 4,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "131313":
        {
            "Name": "Alexandra Daddario",
            "Major": "Data Finance",
            "Enrolling_Year": "2021",
            "Total_attendance": 0,
            "Standing": 5.0,  # G for good
            "Year": 5,
            "Last_attendance_time": "2023-01-01 01:01:01"

        },
    "141414":
        {
            "Name": "Tony Stark",
            "Major": "Computer Science",
            "Enrolling_Year": "2023",
            "Total_attendance": 0,
            "Standing": 3.0,  # G for good
            "Year": 1,
            "Last_attendance_time": "2023-01-01 01:01:01"

        }



}
ref.child('Computer Science').set(data)
ref.child('Informatics').set(data2)
ref.child('Computer Architecture').set(data3)


# This is how we unzip json data dictionary in python
# for key, value in data.items():
#     ref.child(key).set(value)  # we use child if we want to send data to specific directory
# for key, value in data2.items():
#     ref.child(key).set(value)  # we use child if we want to send data to specific directory