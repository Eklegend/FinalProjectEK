import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

# Here we will link the storage to process our images

cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "ekfacialrecognition.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
# here we are using default camera sizing, either 1280*720, 640*480 or 320*240 or 160*120
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/fullscope.png')

# import the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encoding Files")
file = open("EncodeFile.p", "rb")  # rb is read in binary mode
encodeListKnownWithIds = pickle.load(file)  # will add all the list and info here
file.close()

# extracts the information in two parts, and send to encodeListKnownWithIds for pickle to load
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode Files Loaded")

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()

    # scale the image smaller
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    imgBackground[137:137 + 480, 61:61 + 640] = img
    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]

    # Faces in the current Frame
    faceCurrentFrame = face_recognition.face_locations(imgS)  # location of our images
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)  # this will find the encoding of face

    if faceCurrentFrame:

        # loops through the encoding to see a match
        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            # the lower the best distance the better the match is
            facialDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("Matches", matches)
            # print("FacialDistance", facialDistance)

            # match the index of the least values
            matchIndex = np.argmin(facialDistance)  # here we are finding the minimum value in the list of Index
            # The reason to find minimum value is that when our faces are a match, it shows the least value for it.

            # print("Match Index",matchIndex) #  here once the minimum values is found that matches the pre-uploaded image,

            # If the minimum value from matchIndex matches our face, it will output Known face detected
            if matches[matchIndex]:
                # print("Known face detected")

                # print(studentIds[matchIndex]) # Now we will output the id of the student of the matched face

                y1, x2, y2, x1 = faceLocation
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 61 + x1, 137 + y1, x2 - x1, y2 - y1  # here we use the measurements of the imgBackground
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (265, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            # above we have set counter = 0. Once theres a face match, counter will chance to 1 ( only once)q
            # once counter ==1, it will get the Students id and prints student info

            if counter == 1:
                # Gets the student info (data)
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # This is output the image that we need
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imageStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Resize image automatically
                imageStudent = cv2.resize(imageStudent, (362, 245))
                # Update data of attendance

                # This converts the date time from string to object
                datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)

                # This secondsElapsed makes the user to only get attended after the seconds written
                # Here 82800 seconds is equal to 23 hours. Thus, User can on scan the image after 23 hours
                if secondsElapsed > 82800:

                    ref = db.reference(f'Students/{id}')
                    studentInfo['Total_attendance'] += 1
                    ref.child('Total_attendance').set(studentInfo['Total_attendance'])
                    ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType = 3
                    counter = 0
                    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]
                    imageStudent = cv2.resize(imageStudent, (362, 245))

            if modeType != 3:  # This ensures that the below code only runs when mode type is 0,1,2

                # Creates a timer that shows that the student image is already marked

                if 10 < counter < 20:
                    modeType = 2
                imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]

                if counter <= 10:
                    # here we are positioning the data accordingly
                    cv2.putText(imgBackground, str(studentInfo['Total_attendance']), (868, 88),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['Major']), (973, 548),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(id), (916, 485),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['Standing']), (983, 655),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (853, 655),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['Enrolling_Year']), (1113, 655),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)

                    # centering the name
                    (w, h), _ = cv2.getTextSize(studentInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 0.8, 2)
                    offset = (468 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['Name']), (805 + offset, 427),  # the position
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)

                    # Here we call the image to display
                    imgBackground[138:138 + 245, 840:840 + 362] = imageStudent

                    # Resize image automatically
                    imageStudent = cv2.resize(imageStudent, (362, 245))

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imageStudent = []
                    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    #  imgBackground[y_offset:y_offset + region_height, x_offset:x_offset + region_width] = img
    imgBackground[137:137 + 480, 61:61 + 640] = img

    # imgModeList[0] = Full details, imgModeList[1] = Active, imgModeList[2] = Marked, imgModeList[3] = Already Marked
    # here we are joining Image from the Modes to the main (background)
    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
