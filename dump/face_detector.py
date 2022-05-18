from faceapp.models import Student
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime
import functools
import operator
import face_recognition




# def face_recognition():
#     camera = cv2.VideoCapture(0)
#     while True():
#         success, image = camera.read()
#         if not success:
#             break
#         else:
#             image = recognizer(image, trained_classifier, face_cascade)

#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     trained_classifier = cv2.face.LBPHFaceRecognizer_create()
#     trained_classifier.read('classifier.xml')
    

#     def attendance(student_id, roll_no, student_name):
#         with open('attendance.csv', 'r+', newline='\n') as file:
#             data_list = file.readlines()
#             name_list = []
#             for line in data_list:
#                 entry = line.split((','))
#                 name_list.append(entry[0])

#             if((student_id not in name_list) and (roll_no not in name_list) and (student_name not in name_list)):
#                 now = datetime.now()
#                 date_str = now.strftime ('%d/%m/%Y')
#                 time_str = now.strftime('%H:%M:%S')
#                 file.writelines(f'\n{student_id}, {roll_no}, {student_name}, {time_str}, {date_str}, Present')
                
#     def draw_box(image, classifier, scale_factor, min_neighbour, color, text, trained_classifier):
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         descriptors = classifier.detectMultiScale(gray_image, scale_factor, min_neighbour)

#         coordinates = []

#         for (x, y, w, h) in descriptors:
#             cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             id, predict = trained_classifier.predict(gray_image[y:y+h, x:x+w])
#             confidence = int((100 * (1-predict / 300)))

#             result = Student.query.get(id)
            
#             if result:
#                 student_name = result.name
#                 roll_no = result.roll_no
#                 student_id = result.id

#             if confidence > 80:
#                 cv2.putText(image, f'ID: {student_id}', (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 cv2.putText(image, f'Roll No.: {roll_no}', (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 cv2.putText(image, f'Name: {student_name}', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 attendance(student_id, roll_no, student_name)
#             else:
#                 cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
#                 cv2.putText(image, 'Unknown Face', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

#             coordinates = [x, y, w, h]
#         return coordinates


#     def recognizer(image, trained_classifier, face_cascade):
#         coordinates = draw_box(image, face_cascade, 1.1, 10, (255, 25, 255), 'Face', trained_classifier)
        
                


            # ret, buffer = cv2.imencode('.jpg', image)
            # image = buffer.tobytes()
            # yield (b'--frame\r\n'
            #         b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
   
    #     if cv2.waitKey(1) == 13:
    #         break
    # camera.release()
    # cv2.destroyAllWindows()
def face_recog():
        path = 'uploads'
        images = []
        names = []
        myList = os.listdir(path)
        for cl in myList:
                curr_img = cv2.imread(f'{path}/{cl}')
                images.append(curr_img)
                names.append(os.path.splitext(cl)[0].split('.')[1])
        # print(names)

        def find_encodings(images):
                encode_list = []
                for img in images:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)[0]
                        encode_list.append(encode)
                return encode_list

        def mark_attendance(name):
                with open ('Attendance.csv', 'r+') as f:
                        my_data_list = f.readlines()
                        name_list = []
                        for line in my_data_list:
                                entry = line.split()
                                name_list.append(entry[0])
                        if name not in name_list:
                                now = datetime.now()
                                dtString = now.strftime('%H:%M:%S')
                                f.writelines(f'\n{name},{dtString}')



        encode_list_known = find_encodings(images)
# print(len(encode_list_known))

        cam = cv2.VideoCapture(0)


        while True:
                success, img = cam.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                faces_curr_frame = face_recognition.face_locations(imgS)
                encode_curr_frame = face_recognition.face_encodings(imgS, faces_curr_frame)

                for encode_face, face_loc in zip(encode_curr_frame, faces_curr_frame):
                        matches = face_recognition.compare_faces(encode_list_known, encode_face)
                        face_dist = face_recognition.face_distance(encode_list_known, encode_face)
                        match_index = np.argmin(face_dist)

                        if matches[match_index]:
                                name = names[match_index]
                                y1, x2, y2, x1 = face_loc
                                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                cv2.rectangle (img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.rectangle (img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                                mark_attendance(name)


                ret, buffer = cv2.imencode('.jpg', img)
                img = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
