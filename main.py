import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

############################################################ encodeKnown block
path = 'imgbase'
imagesKnown = []
classNames = []
myList = os.listdir(path)
# print(myList)

# read images from folder
for cl in myList:
    currentImg = cv2.imread(f'{path}/{cl}')
    imagesKnown.append(currentImg)
    classNames.append(os.path.splitext(cl)[0])
    # print(classNames)


# findEncodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(imagesKnown)
print('Encoding Complete')

################################################################ csv file handling block
g = open('Attendance.csv', 'r+')
DataList = g.readlines()
nameList = []

# sort bullshit from csv
for i in range(len(DataList)):
    if DataList[-i - 1] == '\n':
        DataList.pop(-i - 1)

# print(DataList)

headerList = DataList[0].split(',')
headerList[-1] = headerList[-1].split()[0]
DataList.pop(0)

# nameList creation from DataList
for line in DataList:
    line = line.replace('\n', '')
    entry = line.split(',')
    nameList.append(entry)

# print(nameList)

# modifying header for csv
headerStr = f'{headerList[0]},{headerList[1]}'

for i in range(len(headerList) - 2):
    headerStr += f',{headerList[i + 2]}'
if headerList[-1] != f'{datetime.now().strftime("%d/%m/%y")}':
    headerStr += f',{datetime.now().strftime("%d/%m/%y")}\n'
else:
    headerStr += f'\n'

g.seek(0)
g.writelines(headerStr)

# appending nameList
if len(nameList[0]) < len(headerStr.split(',')):
    for i in range(len(nameList)):
        nameList[i].append('A')


# print(nameList)


def rewrite():
    global headerStr
    global nameList
    g.seek(0)
    g.writelines(headerStr)

    for i in range(len(nameList)):
        tempStr = f'{nameList[i][0]},{nameList[i][1]}'
        for j in range(len(nameList[i]) - 3):
            tempStr += f',{nameList[i][j + 3]}'
        tempStr += f',{nameList[i][-1]}\n'
        g.writelines(tempStr)


def markAttendance(name):
    global DataList
    global nameList

    for n in range(len(nameList)):
        if nameList[n][1] == name:
            nameList[n][-1] = 'P'
            break

    rewrite()


rewrite()

############################################################## live video feed block
cap = cv2.VideoCapture(0)

while True:
    # timeNow = datetime.now()

    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
