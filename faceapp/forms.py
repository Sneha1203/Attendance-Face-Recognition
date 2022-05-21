from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from faceapp.models import User, Student

DEPT_CHOICES =['Select Department: ', 'CSE', 'IT']
COURSE_CHOICES = ['Select Course: ', 'BE', 'FE', 'TE']
YEAR_CHOICES = ['Select Year: ', '2020-21', '2021-22', '2022-23', '2023-24']
SEMESTER_CHOICES = ['Select Semester: ', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
SECTION_CHOICES = ['Select Section: ', 'CSE-1', 'CSE-2', 'IT-1', 'IT-2']
GENDER_CHOICES = ['Select Gender: ', 'Male', 'Female', 'Other', 'Prefer not to say']


class LoginUserForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')



class RegisterUserForm(FlaskForm):

    def validate_username(self, username_to_Check):
        user = User.query.filter_by(username=username_to_Check.data).first()
        if user:
            raise ValidationError('Username Already Exists! Try Different Username!')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Aready Exists! Try different Email!')

    username = StringField(label='Username: ', validators=[Length(min=2, max=10), DataRequired()])
    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class RegisterStudentForm(FlaskForm):

    # def validate_email(self, email_to_check):
    #     email = Student.query.filter_by(email=email_to_check.data).first()
    #     if email:
    #         raise ValidationError('Email Aready Exists! Try different Email!')

    # def validate_roll_no(self, roll_no_to_check):
    #     roll_no = Student.query.filter_by(roll_no=roll_no_to_check.data).first()
    #     if roll_no:
    #         raise ValidationError('Roll Number Aready Exists! Try with a different one!')


    dept = SelectField(label='Department: ', validators=[DataRequired()], choices=DEPT_CHOICES)
    course = SelectField(label='Course: ', validators=[DataRequired()], choices=COURSE_CHOICES)
    year = SelectField(label='Year: ', validators=[DataRequired()], choices=YEAR_CHOICES)
    semester = SelectField(label='Semester: ', validators=[DataRequired()], choices=SEMESTER_CHOICES)
    name = StringField(label='Student Name: ', validators=[Length(max=30),DataRequired()])
    section = SelectField(label='Section: ', validators=[DataRequired()], choices=SECTION_CHOICES)
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    gender = SelectField(label='Gender: ', validators=[DataRequired()], choices=GENDER_CHOICES)
    mobile_no = StringField(label='Mobile Number: ', validators=[Length(10), DataRequired()])
    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    teacher = StringField(label='Teacher: ', validators=[Length(min=2, max=20),DataRequired()])
    submit = SubmitField(label='Register Student')


class UploadForm(FlaskForm):
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    photo_sample = FileField(label='Upload a Photo: ', validators=[DataRequired()])
    submit = SubmitField(label='Upload')
    
    

class FilterAttendanceForm(FlaskForm):
    year = SelectField(label='Year: ', validators=[DataRequired()], choices=YEAR_CHOICES)
    dept = SelectField(label='Department: ', validators=[DataRequired()], choices=DEPT_CHOICES)
    semester = SelectField(label='Semester: ', validators=[DataRequired()], choices=SEMESTER_CHOICES)
    teacher = StringField(label='Teacher: ', validators=[Length(min=2, max=20),DataRequired()])
    course = SelectField(label='Course: ', validators=[DataRequired()], choices=COURSE_CHOICES)
    section = SelectField(label='Section: ', validators=[DataRequired()], choices=SECTION_CHOICES)
    submit = SubmitField(label='Filter Attendance')


class StudentAttendanceForm(FlaskForm):
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    submit = SubmitField(label='Show Attendance')
