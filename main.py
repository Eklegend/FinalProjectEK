import os
import cv2

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
print(len(imgModeList))

while True:
    success, img = cap.read()

    #  imgBackground[y_offset:y_offset + region_height, x_offset:x_offset + region_width] = img
    imgBackground[137:137 + 480, 61:61 + 640] = img

    # imgModeList[0] = Full details, imgModeList[1] = Active, imgModeList[2] = Marked, imgModeList[3] = Already Marked
    # here we are joining Image from the Modes to the main (background)
    imgBackground[0:0 + 720, 757:757 + 523] = imgModeList[0]

    cv2.imshow("Face Attendance", imgBackground)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
