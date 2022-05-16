from email.mime import image
from faceapp import app
from faceapp import db
from flask import render_template, redirect, url_for, flash, request, Response
from faceapp.face_detector import face_recognition
from faceapp.models import User, Student
from faceapp.forms import LoginUserForm, RegisterStudentForm, RegisterUserForm, UploadForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
from datetime import datetime
import os 
import cv2
from PIL import Image
import numpy as np
from faceapp.train_data import train_images
from faceapp.face_detector import face_recog
          

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/register_student', methods=["GET", "POST"])
@login_required
def register_student():
    form = RegisterStudentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            create_student = Student(dept=form.dept.data,
                                    course=form.course.data,
                                    year=form.year.data,
                                    semester=form.semester.data,
                                    name=form.name.data,
                                    section=form.section.data,
                                    roll_no=form.roll_no.data,
                                    gender=form.gender.data,
                                    mobile_no=form.mobile_no.data,
                                    email=form.email.data,
                                    teacher=form.teacher.data)
            db.session.add(create_student)
            db.session.commit()
            flash(f'Student has been registered succesfully!', category='success')
            return redirect(url_for('upload_photo'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with registering the student: {err_msg}',category='danger')
    return render_template('register_student.html', form=form)



@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    form = UploadForm()
    if form.validate_on_submit():
        photo_to_upload = Student(roll_no=form.roll_no.data,
                                  photo_sample=form.photo_sample.data)

        student = Student.query.get(form.roll_no.data)

        file_name = photo_to_upload.photo_sample.filename
        pic_name = 'Student' + '.' + str(student.id) + '.' + file_name
        saver = request.files['photo_sample']
        saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

        
        student.photo_sample = pic_name
        db.session.commit()            
    return render_template('upload_photo.html', form=form)



@app.route('/student_details', methods=['GET', 'POST'])
@login_required
def student_details():
    # form = RegisterStudentForm()
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         create_student = Student(dept=form.dept.data,
    #                                 course=form.course.data,
    #                                 year=form.year.data,
    #                                 semester=form.semester.data,
    #                                 name=form.name.data,
    #                                 section=form.section.data,
    #                                 roll_no=form.roll_no.data,
    #                                 gender=form.gender.data,
    #                                 mobile_no=form.mobile_no.data,
    #                                 email=form.email.data,
    #                                 teacher=form.teacher.data)

            # pic = secure_filename(create_student.photo_sample.filename)
            # # pic_filename = request.files[form.photo_sample.name].read()
            # create_student.photo_sample = pic
            # db.session.add(create_student)
            # # db.session.commit()
            # # pic_name = str(uuid.uuid1()) + "_" + pic_filename

            # id = 0
            # students = Student.query.all()

            # for student in students:
            #     id+=1
            #     if student.roll_no == create_student.roll_no:
            #         pic_name = 'uploads/' + str(id) + "." + pic
            #         saver = request.files['photo_sample']
            #         saver = cv2.cvtColor(saver, cv2.COLOR_BGR2GRAY)
            #         cv2.imwrite(pic_name, saver)
            #         student.photo_sample = pic_name
            #         db.session.commit()
                # db.session.add(create_student)

            # id += 1
    #         flash(f'Student has been registered succesfully!', category='success')
    #         return redirect(url_for('student_details'))
    #     if form.errors != {}:
    #         for err_msg in form.errors.values():
    #             flash(f'There was an error with registering the student: {err_msg}',category='danger')
    # if request.method == 'GET':
        students = Student.query.all()
        return render_template('student_details.html', students=students)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcome {attempted_user}! You have logged in successfully!', category='success')
            return redirect(url_for('profile'))
        else:
            flash(f'Username and password do not match! Please try again!', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        create_user = User(username=form.username.data,
                            email=form.email.data,
                            password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f'Account created successfully! You are logged in as {create_user.username}!', category='success')
        return redirect(url_for('profile'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out successfully!', category='info')
    return redirect(url_for('home'))


@app.route('/attendance_details')
def attendance_details():
    return render_template('attendance_details.html')


@app.route('/train_data')
def train_data():
    # data_dir = ('uploads')
    # path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        
    # faces = []
    # ids = []

    # for image_path in path:
    #     # img = cv2.imread(image)
    #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     img = Image.open(image_path).convert('L')    # conversion to grayscale image
    #     image_np = np.array(img, 'uint8')
    #     # img_path = os.path.split(image)[1]
    #     # id = Student.query.filter_by(photo_sample=img_path).first()
    #     # id = int(((os.path.split(image_path)[1]).split('.')[1]).split('_')[0])
    #     id = int(image_path.split(".")[1])
        

    #     faces.append(image_np)
    #     ids.append(id)
    #     # cv2.imshow('Training', image_np)
    #     cv2.waitKey(1) == 13
    # ids = np.array(ids)
    # # labels=[0]*len(faces)

    # classifier = cv2.face.LBPHFaceRecognizer_create()
    # classifier.train(faces, ids)
    # classifier.write('classifier.xml')

    # cv2.destroyAllWindows()
    train_images()
    flash(f'Data Sets Trained Successfully!', category='success')
    return render_template('train_data.html')


# def attendance(id, roll_no, name):
#     with open('attendance.csv', 'r+', newline='\n') as file:
#         data_list = file.readlines()
#         name_list = []
#         for line in data_list:
#             entry = line.split((','))
#             name_list.append(entry[0])

#         if((id not in name_list) and (roll_no not in name_list) and (name not in name_list)):
#             now = datetime.now()
#             date_str = now.strftime ('%d/%m/%Y')
#             time_str = now.strftime('%H:%M:%S')
#             file.writelines(f'\n{id}, {roll_no}, {name}, {time_str}, {date_str}, Present')

# def draw_box(image, classifier, scale_factor, min_neighbour, color, text, trained_classifier):
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     descriptors = classifier.detectMultiScale(gray_image, scale_factor, min_neighbour)

#     coordinates = []

#     for (x, y, w, h) in descriptors:
#         cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         id, predict = trained_classifier.predict(gray_image[y:y+h, x:x+w])
#         confidence = int((100 * (1-predict/ 300)))

#         result = Student.query.get(id)
     
#         if result:
#             student_name = result.name
#             roll_no = result.roll_no
#             student_id = result.id

#             if confidence > 70:
#                 cv2.putText(image, f'ID: {student_id}', (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 cv2.putText(image, f'Roll No.: {roll_no}', (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 cv2.putText(image, f'Name: {student_name}', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
#                 attendance(student_id, roll_no, student_name)
#                 break
#         else:
#             cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
#             cv2.putText(image, 'Unknown Face', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

#         coordinates = [x, y, w, h]
#     return coordinates


# def recognizer(image, trained_classifier, face_cascade):
    
#     return image

# camera = cv2.VideoCapture(0)

def gen_frames():
    path = 'uploads'
    images = []
    roll_nos = []
    names = []
    myList = os.listdir(path)
    for cl in myList:
            curr_img = cv2.imread(f'{path}/{cl}')
            images.append(curr_img)
            roll_nos.append(os.path.splitext(cl)[0].split('.')[1])
            names.append(os.path.splitext(cl)[0].split('.')[2])
    # print(names)

    def find_encodings(images):
            encode_list = []
            for img in images:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    encode = face_recognition.face_encodings(img)[0]
                    encode_list.append(encode)
            return encode_list

    def mark_attendance(roll, name):
            with open ('Attendance.csv', 'r+') as f:
                    my_data_list = f.readlines()
                    roll_list = []
                    for line in my_data_list:
                            entry = line.split()
                            roll_list.append(entry[0])
                    if roll not in roll_list:
                            now = datetime.now()
                            dtString = now.strftime('%H:%M:%S')
                            f.writelines(f'\n{roll},{name}, {dtString}')



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
                            roll = roll_nos[match_index]
                            name = names[match_index]
                            y1, x2, y2, x1 = face_loc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            cv2.rectangle (img, (x1, y1), (x2, y2), (128, 0, 128), 2)
                            cv2.rectangle (img, (x1, y2+90), (x2, y2), (128, 0, 128), cv2.FILLED)
                            cv2.putText(img, f'ROLL NO: {roll}', (x1+6, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            cv2.putText(img, f'NAME: {name}', (x1+12, y2+60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            mark_attendance(roll, name)


            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
    # while True:
    #     success, image = camera.read()
    #     if not success:
    #         break
    #     else: 
    #         face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #         trained_classifier = cv2.face.LBPHFaceRecognizer_create()

    #         trained_classifier.read('classifier.xml')

    #         # coordinates = draw_box(image, face_cascade, 1.1, 10, (255, 25, 255), 'Face', trained_classifier)
    #         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #         descriptors = face_cascade.detectMultiScale(gray_image, 1.1, 10)

    #         coordinates = []

    #         for (x, y, w, h) in descriptors:
    #             cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #             id, predict = trained_classifier.predict(gray_image[y:y+h, x:x+w])
    #             confidence = int((100 * (1-predict/ 300)))

    #             result = Student.query.get(id)
            
    #             if result:
    #                 student_name = result.name
    #                 roll_no = result.roll_no
    #                 student_id = result.id

    #                 if confidence > 70:
    #                     cv2.putText(image, f'ID: {student_id}', (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
    #                     cv2.putText(image, f'Roll No.: {roll_no}', (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
    #                     cv2.putText(image, f'Name: {student_name}', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
    #                     with open('attendance.csv', 'r+', newline='\n') as file:
    #                         data_list = file.readlines()
    #                         name_list = []
    #                         for line in data_list:
    #                             entry = line.split((','))
    #                             name_list.append(entry[0])

    #                         if((student_id not in name_list) and (roll_no not in name_list) and (student_name not in name_list)):
    #                             now = datetime.now()
    #                             date_str = now.strftime ('%d/%m/%Y')
    #                             time_str = now.strftime('%H:%M:%S')
    #                             file.writelines(f'\n{student_id}, {roll_no}, {student_name}, {time_str}, {date_str}, Present')
                                            
    #                         else:
    #                                     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
    #                                     cv2.putText(image, 'Unknown Face', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

    #             coordinates = [x, y, w, h]
    #         ret, buffer = cv2.imencode('.jpg', image)
    #         image = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #                 b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/take_attendance')
def take_attendance():
    # face_recog()
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')









                        

# def gen_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             def recognizer(image, trained_classifier, face_cascade):
#                 coordinates = draw_box(image, face_cascade, 1.1, 10, (255, 25, 255), 'Face', trained_classifier)
#                 return image

#             face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#             trained_classifier = cv2.face.LBPHFaceRecognizer_create()
#             trained_classifier.read('classifier.xml')

        
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = recognizer(frame, trained_classifier, face_cascade)
#             # frame = buffer.tobytes()
        
#             # yield(b'--frame\r\n'
#             #     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#             if cv2.waitKey(1) == 13:
#                 break

#             camera.release()
#             cv2.destroyAllWindows()
