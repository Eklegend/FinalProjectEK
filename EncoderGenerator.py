# HERE WE GENERATES THE CODES AND FACE-RECOGNITION

import cv2
import face_recognition
import pickle # this library is a way to store and bring back Python Objects
import os

# import student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList) # this will print the images id in list = ['121212.png', '131313.png', '141414.png']

imgList = []
# get the id of student
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])  # This splits the png from the image name, we write [0] because
    # from ('121212', '.png') , we want the 121212 which value is [0]

print(studentIds) # will output ['121212', '131313', '141414']