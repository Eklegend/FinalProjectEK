# HERE WE GENERATES THE CODES AND FACE-RECOGNITION

import cv2
import face_recognition
import pickle  # this library is a way to store and bring back Python Objects
import os

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
print (encodeListKnown)
print("Encoding Complete")
# once we get the endoing in array format, we need to save it in a pickle file so we can import it.