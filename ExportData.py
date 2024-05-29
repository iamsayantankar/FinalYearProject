import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://final-year-project-nsec-default-rtdb.asia-southeast1.firebasedatabase.app",
    'storageBucket': "final-year-project-nsec.appspot.com"
})

studentInfo = db.reference(f'Students').get()

print(studentInfo)

# Loop through each list of data
for i, data in enumerate(studentInfo):
    # print(i)
    # print(data)
    if type(data) == type(None):
        continue

    try:
        attendanceTiming = data["attendance-timing"]
        attendanceDate = []
        print(data)
        # attendanceDate = [{"auth key": key, "Time": value} for key, value in data.items()]

        for key, value in attendanceTiming.items():
            myData = {"auth-key": key, "Time": value}
            attendanceDate.append(myData)
        # for value in attendanceTiming.values():
        #     attendanceDate.append(value)

        # df = pd.DataFrame(attendanceDate, columns=["attendance-timing"])
        print(attendanceTiming)

        df = pd.DataFrame(attendanceDate)

        excel_file_path = "output_id-" + str(i) + " - " + data["name"] + ".xlsx"
        df.to_excel(excel_file_path, index=False)



    except KeyError:
        print("Key 'city' does not exist in the dictionary")
