from traceback import print_stack
from sqlalchemy import func
from faceapp import app
from faceapp import db
from flask import render_template, redirect, url_for, flash, request, Response
import face_recognition
from faceapp.models import Attendance, User, Student
from faceapp.forms import LoginUserForm, RegisterStudentForm, RegisterUserForm, UploadForm, FilterAttendanceForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os 
import cv2
from PIL import Image
import numpy as np
import pandas as pd

          

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

        student = Student.query.filter_by(roll_no=form.roll_no.data).first()

        file_name = photo_to_upload.photo_sample.filename
        pic_name = 'Student' + '.' + str(student.roll_no) + '.' + file_name
        saver = request.files['photo_sample']
        saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

        
        student.photo_sample = pic_name
        db.session.commit()
        flash(f'Photo has been updated succesfully!', category='success')

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

# def load_data():
#     file_name = 'attendance.csv'
#     colnames = ['roll_no', 'name', 'attendance_date', 'attendance_time']
#     data = pd.read_csv(file_name, names=colnames, skiprows=1)
#     data.sort_values(by=['roll_no', 'attendance_date', 'attendance_time'], inplace=True)
#     data.drop_duplicates(subset=['roll_no', 'attendance_date'], keep='first', inplace=True)
#     data.to_csv('sorted_attendance.csv', header=False, index=False)
#     del data
    

@app.route('/filter_attendance', methods=['GET', 'POST'])
def filter_attendance():
    # load_data()
    # file_name = 'attendance.csv'
    # colnames = ['roll_no', 'name', 'attendance_date', 'attendance_time']
    # data = pd.read_csv(file_name, names=colnames, skiprows=1)
    # data.sort_values(by=['roll_no', 'attendance_date', 'attendance_time'], inplace=True)
    # data.drop_duplicates(subset=['roll_no', 'attendance_date'], keep='first', inplace=True)
    # data.to_csv('sorted_attendance.csv', header=False, index=False)
    # data = np.genfromtxt('sorted_attendance.csv', delimiter=',', skip_header=1, dtype=(int, str, str, str))

    file_name = 'attendance.csv'
    colnames = ['roll_no', 'name', 'attendance_date', 'attendance_time']
    data = pd.read_csv(file_name, names=colnames, skiprows=1)
    data.sort_values(by=['roll_no', 'attendance_date', 'attendance_time'], inplace=True)
    data.drop_duplicates(subset=['roll_no', 'attendance_date'], keep='first', inplace=True)
    data.to_csv('sorted_attendance.csv', header=colnames, index=True)
    
    # attendance_file = open('attendance.csv', 'r+')
    # attendance_file.truncate(1)
    # attendance_file.close()
    
    records = np.genfromtxt('sorted_attendance.csv', delimiter=',', skip_header=1, encoding='utf-8', converters = {0: lambda s: int(s), 1: lambda s: int(s), 2: lambda s: str(s), 3: lambda s: str(s), 4: lambda s: str(s)})
    records = records.tolist()
    for record in records:
        search_record = Attendance.query.filter_by(roll_no=record[1], date=record[3]).first()
        if search_record is None:
            present_student = Student.query.filter_by(roll_no=record[1]).first()
            attendance_record = Attendance(
                id=record[0],
                name=record[2],
                roll_no=record[1],
                time=record[4],
                date=record[3],
                student=present_student.id
            )
            db.session.add(attendance_record)
            db.session.commit()
        else:
            continue

    # sorted_attendance_file = open('sorted_attendance.csv', 'r+')
    # sorted_attendance_file.truncate(1)
    # sorted_attendance_file.close()

    # get data from user through attenance form to filter the attendance
    form = FilterAttendanceForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            dept = form.dept.data
            year = form.year.data
            semester = form.semester.data
            teacher = form.teacher.data
            course = form.course.data
            section = form.section.data
            
            students = Student.query.filter_by(dept=dept, year=year, semester=semester, teacher=teacher, course=course, section=section)

            for student in students:
                roll_to_count = student.roll_no
                no_of_present = Attendance.query.filter_by(roll_no=roll_to_count).count()
                student.days_present = no_of_present
                db.session.commit()
            return redirect(url_for('attendance_details', dept=dept, year=year, semester=semester, teacher=teacher, course=course, section=section, **request.args))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error while fetching attendance details: {err_msg}',category='danger')

    return render_template('filter_attendance.html', form=form)



@app.route('/attendance_details')
def attendance_details():
    dept = request.args.get('dept')
    year = request.args.get('year')
    semester = request.args.get('semester')
    teacher = request.args.get('teacher')
    course = request.args.get('course')
    section = request.args.get('section')
    students = Student.query.filter_by(dept=dept, year=year, semester=semester, teacher=teacher, course=course, section=section)
    # roll_nos = Student.query(Student.roll_no).filter_by(dept=dept, year=year, semester=semester, teacher=teacher, course=course, section=section)
    # attendance = Attendance.query.filter_by(roll_nos).all()
    return render_template('attendance_details.html', students=students, dept=dept, year=year, semester=semester, teacher=teacher, course=course, section=section)


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
            with open ('attendance.csv', 'r+') as f:
                    my_data_list = f.readlines()
                    roll_list = []
                    for line in my_data_list:
                            entry = line.split()
                            roll_list.append(entry[0])
                    if roll not in roll_list:
                            now = datetime.now()
                            attendance_time = now.strftime('%H:%M:%S')
                            attendance_date = now.strftime('%d-%m-%Y')
                            f.writelines(f'\n{roll},{name},{attendance_date},{attendance_time}')



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


