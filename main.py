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

# Here we will link the storage to process our images

cred = credentials.Certificate("serviceAccountKey.json")

# link the realtime database url in json format
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ekfacialrecognition-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "ekfacialrecognition.appspot.com"
})


cap = cv2.VideoCapture(0)
# here we are using default camera sizing, either 1280*720, 640*480 or 320*240 or 160*120
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/BackgrdImage.png')

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

    # Faces in the current Frame
    faceCurrentFrame = face_recognition.face_locations(imgS)  # location of our images
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)  # this will find the encoding of face

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
            #print("Known face detected")

            #print(studentIds[matchIndex]) # Now we will output the id of the student of the matched face

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 61 + x1, 137 + y1, x2 - x1, y2 - y1 # here we use the measurements of the imgBackground
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            id = studentIds[matchIndex]
            if counter == 0 :
                counter =1
                modeType = 1
    if counter != 0:

        # above we have set counter = 0. Once theres a face match, counter will chance to 1 ( only once)
        # once counter ==1, it will get the Students id and prints student info
        if counter ==1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

        cv2.putText(imgBackground,str(studentInfo['Total_attendance']),(868,88), # the position
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
        cv2.putText(imgBackground,str(studentInfo['Name']),(805,424), # the position
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
        cv2.putText(imgBackground,str(studentInfo['Major']),(973,547), # the position
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
        cv2.putText(imgBackground,str(id),(916,479), # the position
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
        cv2.putText(imgBackground, str(studentInfo['Standing']), (980, 655),  # the position
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentInfo['Year']), (849, 655),  # the position
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv2.putText(imgBackground, str(studentInfo['Enrolling_Year']), (1110, 655),  # the position
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

        counter +=1






    cv2.imshow("Face Attendance", imgBackground)
    #  imgBackground[y_offset:y_offset + region_height, x_offset:x_offset + region_width] = img
    imgBackground[137:137 + 480, 61:61 + 640] = img

    # imgModeList[0] = Full details, imgModeList[1] = Active, imgModeList[2] = Marked, imgModeList[3] = Already Marked
    # here we are joining Image from the Modes to the main (background)
    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[modeType]



    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
