from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from faceapp.models import User, Student


# choices for SelectField for department, course, year, semester, section and gender
DEPT_CHOICES =['Select Department: ', 'CSE', 'IT']
COURSE_CHOICES = ['Select Course: ', 'BE', 'TE']
YEAR_CHOICES = ['Select Year: ', '2020-24', '2021-25']
SECTION_CHOICES = ['Select Section: ', 'CSE-1', 'CSE-2', 'IT-1', 'IT-2']
GENDER_CHOICES = ['Select Gender: ', 'Male', 'Female', 'Other', 'Prefer not to say']


# form for user login
class LoginUserForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


# form for registering the user
class RegisterUserForm(FlaskForm):

    # function to check if the entered username is already in use or not
    def validate_username(self, username_to_Check):
        user = User.query.filter_by(username=username_to_Check.data).first()
        if user:
            raise ValidationError('Username Already Exists! Try Different Username!')

    # function to check if the entered email is already in use or not
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Aready Exists! Try different Email!')

    username = StringField(label='Username: ', validators=[Length(min=2, max=10), DataRequired()])
    first_name = StringField(label='First Name: ', validators=[Length(min=2, max=15), DataRequired()])
    last_name = StringField(label='Last Name: ', validators=[Length(min=2, max=15), DataRequired()])
    dept = SelectField(label='Department: ', validators=[DataRequired()], choices=DEPT_CHOICES)
    gender = SelectField(label='Gender: ', validators=[DataRequired()], choices=GENDER_CHOICES)
    mobile_no = StringField(label='Mobile Number: ', validators=[Length(10), DataRequired()])
    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


# form for registering student
class RegisterStudentForm(FlaskForm):
    dept = SelectField(label='Department: ', validators=[DataRequired()], choices=DEPT_CHOICES)
    course = SelectField(label='Course: ', validators=[DataRequired()], choices=COURSE_CHOICES)
    year = SelectField(label='Year: ', validators=[DataRequired()], choices=YEAR_CHOICES)
    name = StringField(label='Student Name: ', validators=[Length(max=30),DataRequired()])
    section = SelectField(label='Section: ', validators=[DataRequired()], choices=SECTION_CHOICES)
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    gender = SelectField(label='Gender: ', validators=[DataRequired()], choices=GENDER_CHOICES)
    mobile_no = StringField(label='Mobile Number: ', validators=[Length(10), DataRequired()])
    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    teacher = StringField(label='Teacher: ', validators=[Length(min=2, max=20),DataRequired()])
    submit = SubmitField(label='Register Student')


# form for uploading sample photo of a particular student
class UploadForm(FlaskForm):
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    photo_sample = FileField(label='Upload a Photo: ', validators=[DataRequired()])
    submit = SubmitField(label='Upload')


# form for displaying the attendance of a particular student
class DisplayByRollForm(FlaskForm):
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    submit = SubmitField(label='Show Attendance')


# form for displaying the attendance of a class
class DisplayByClassForm(FlaskForm):
    year = SelectField(label='Year: ', validators=[DataRequired()], choices=YEAR_CHOICES)
    dept = SelectField(label='Department: ', validators=[DataRequired()], choices=DEPT_CHOICES)
    teacher = StringField(label='Teacher: ', validators=[Length(min=2, max=20),DataRequired()])
    course = SelectField(label='Course: ', validators=[DataRequired()], choices=COURSE_CHOICES)
    section = SelectField(label='Section: ', validators=[DataRequired()], choices=SECTION_CHOICES)
    date = StringField(label='Date: ', validators=[Length(min=2, max=20),DataRequired()])
    submit = SubmitField(label='Show Attendance')


# form to download attendance records of a student as csv file
class StudentAttendanceCSVForm(FlaskForm):
    submit = SubmitField(label='Download Attendance')


# form to download attendance records of a class as csv file
class ClassAttendanceCSVForm(FlaskForm):
    submit = SubmitField(label='Download Attendance')
