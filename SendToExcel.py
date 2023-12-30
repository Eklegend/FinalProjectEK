import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
from course_selector import choose_course

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/"
})

course_name = choose_course()
# Access a reference to your Firebase database
ref = db.reference(f'Courses/{course_name}')


def update_excel_file(event):
    firebase_data = ref.get()
    # Check if data is fetched
    if not firebase_data:
        print(f"No data available for the selected course '{course_name}'.")
        return

    # Extract Keys and values
    student_ids = list(firebase_data.keys())
    student_data = [firebase_data[student_id] for student_id in student_ids]

    # Transform Firebase data into a Pandas DataFrame
    df = pd.DataFrame(student_data, index=student_ids)

    # Write data to Excel file using Pandas
    excel_file_path = f'{course_name}_StudentData.xlsx'
    df.to_excel(excel_file_path, index_label='StudentID')

    print(f"Data for course '{course_name}' has been exported to '{excel_file_path}'")


# Attach a listener to the reference
ref.listen(update_excel_file)
