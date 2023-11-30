import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Access a reference to your Firebase database
ref = db.reference('Students')

# Retrieve data from Firebase
firebase_data = ref.get()


def update_excel_file(event):
    firebase_data = ref.get()
    # Extract Keys and values
    keys = []
    values = []
    for key, value in firebase_data.items():
        keys.append(key)
        values.append(value)

    # Transform Firebase data into a Pandas DataFrame
    # For example, assuming you have fetched a dictionary of data
    # Convert it into a DataFrame for easy manipulation
    df = pd.DataFrame({'Keys': keys, 'Values': values})

    # Write data to Excel file using Pandas
    excel_file_path = 'StudentData.xlsx'
    df.to_excel(excel_file_path, index=False)

    print(f"Data has been exported to '{excel_file_path}'")


# this listens to updates and updates the excel file
ref.listen(update_excel_file)
