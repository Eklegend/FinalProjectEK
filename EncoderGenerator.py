# HERE WE GENERATE THE CODES AND FACE-RECOGNITION

import cv2
import face_recognition
import pickle  # this library is a way to store and bring back Python Objects
import os
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

# import student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)  # this will print the images id in list = ['121212.png', '131313.png', '141414.png']

imgList = []
# get the id of student
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])  # This splits the png from the image name, we write [0] because
    # from ('121212', '.png') , we want the 121212 which value is [0]

    # here we are linking the images with our database storage
    fileName=f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)  # will output ['121212', '131313', '141414']


def findEncodings(listOfImages):
    # we are putting
    encodeList = []
    for img in listOfImages:
        # opencv uses bgr and face-recognition uses rgb. So we must convert from bgr to rgb
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # this converts
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)  # loops to through the images and save it
    return encodeList


print("Encoding Started")
# call the function above function of the known faces
encodeListKnown = findEncodings(imgList)  # this will generate the image list and saves here in findEncodings

# to tell which id belongs to which encoding
encodeListKnownWithIds = [encodeListKnown, studentIds]

print(encodeListKnown)
# we get the encoding in array format, we need to save it in a pickle file so we can import it when we are using webcam
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')  # we create a file called EncodeFile.p in write in binary mode (wb)
pickle.dump(encodeListKnownWithIds, file)  # we send the file to pickle
file.close()
print("File saved")
