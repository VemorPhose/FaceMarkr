import cv2
import numpy as np
import face_recognition

img1 = face_recognition.load_image_file('imgbase/elon1.webp')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = face_recognition.load_image_file('imgbase/elon4.jfif')
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

faceLoc1 = face_recognition.face_locations(img1)[0]
faceEnc1 = face_recognition.face_encodings(img1)[0]
cv2.rectangle(img1,(faceLoc1[3],faceLoc1[0]),(faceLoc1[1],faceLoc1[2]),(0,255,255),2)

faceLoc2 = face_recognition.face_locations(img2)[0]
faceEnc2 = face_recognition.face_encodings(img2)[0]
cv2.rectangle(img2,(faceLoc2[3],faceLoc2[0]),(faceLoc2[1],faceLoc2[2]),(0,255,255),2)

results = face_recognition.compare_faces([faceEnc1],faceEnc2)
faceDis = face_recognition.face_distance([faceEnc1],faceEnc2)
print(results)
print(faceDis)

cv2.imshow('elon1', img1)
cv2.imshow('elon2', img2)
cv2.waitKey(0)