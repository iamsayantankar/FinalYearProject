import os
import pickle
import time

import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://final-year-project-nsec-default-rtdb.asia-southeast1.firebasedatabase.app",
    'storageBucket': "final-year-project-nsec.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)

cap.set(3, 240)
cap.set(4, 320)

imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[220:220 + 240, 140:140 + 320] = img
    imgBackground[200:200 + 400, 675:675 + 240] = imgModeList[modeType]

    # print(faceCurFrame)
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            print("Match Index", matchIndex)

            if matches[matchIndex]:
                print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                # imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (250, 350))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                # print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                # print(secondsElapsed)
                if studentInfo['last_attendance_date'] != datetime.now().strftime("%Y-%m-%d"):
                # if secondsElapsed > 20:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child("attendance-timing").push(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ref.child('last_attendance_date').set(datetime.now().strftime("%Y-%m-%d"))
                else:
                    modeType = 2
                    counter = 0
                    imgBackground[200:200 + 400, 675:675 + 240] = imgModeList[modeType]
                    cv2.putText(imgBackground, "Already Completes !!!", (675, 445),
                                cv2.FONT_HERSHEY_COMPLEX, .50, (50, 50, 50), 1)
                    time.sleep(2)
                    modeType = 1

        if modeType != 2:

            if 10 < counter < 20:
                modeType = 2

            imgBackground[200:200 + 400, 675:675 + 240] = imgModeList[modeType]

            if counter <= 10:
                cv2.putText(imgBackground, "Joining Year: " + str(studentInfo['starting_year']), (675, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 0.4, (100, 100, 100), 1)

                cv2.putText(imgBackground, "Name: " + str(studentInfo['name']), (675, 445),
                            cv2.FONT_HERSHEY_COMPLEX, .50, (50, 50, 50), 1)

                imgBackground[250:250 + 100, 715:715 + 100] = imgStudent
                # time.sleep(5)

            counter += 1

            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[200:200 + 400, 675:675 + 240] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(2)
