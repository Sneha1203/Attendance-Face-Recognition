from faceapp import app
from faceapp import db
from flask import render_template, redirect, url_for, flash, request, Response
import face_recognition
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
                            attendance_time = now.strftime('%H:%M:%S')
                            attendance_date = now.strftime('%d-%m-%Y')
                            f.writelines(f'\n{roll}, {name}, {attendance_date}, {attendance_time}')



    encode_list_known = find_encodings(images)

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
                            # name = names[match_index]
                            result = Student.query.filter_by(roll_no=roll).first()
                            name = result.name
                            y1, x2, y2, x1 = face_loc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            cv2.rectangle (img, (x1, y1), (x2, y2), (128, 0, 128), 2)
                            # cv2.rectangle (img, (x1, y2+90), (x2, y2), (128, 0, 128), cv2.FILLED)
                            cv2.putText(img, f'ROLL NO: {roll}', (x1+6, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                            cv2.putText(img, f'NAME: {name}', (x1+12, y2+60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                            mark_attendance(roll, name)


            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
  



@app.route('/take_attendance')
def take_attendance():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


