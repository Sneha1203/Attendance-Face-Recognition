from faceapp import bcrypt
from faceapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=10), unique=True, nullable=False)
    first_name = db.Column(db.String(length=15), nullable=False)
    last_name = db.Column(db.String(length=15), nullable=False)
    dept = db.Column(db.String(length=10), nullable=False)
    gender = db.Column(db.String(length=20), nullable=False)
    mobile_no = db.Column(db.String(length=10), unique=True, nullable=False)
    email = db.Column(db.String(length=20), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'{self.username}'



class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    days_present = db.Column(db.Integer(), nullable=True, default=0)
    dept = db.Column(db.String(length=10), nullable=False)
    course = db.Column(db.String(length=10), nullable=False)
    year = db.Column(db.String(length=20), nullable=False)
    name = db.Column(db.String(length=30), nullable=False)
    section = db.Column(db.String(length=10), nullable=False)
    roll_no = db.Column(db.Integer(), unique=True, nullable=False)
    gender = db.Column(db.String(length=20), nullable=False)
    mobile_no = db.Column(db.String(length=10), nullable=False)
    email = db.Column(db.String(length=20), unique=True, nullable=False)
    teacher = db.Column(db.String(length=20), nullable=False)
    photo_sample = db.Column(db.String(), nullable=True, default='NONE')
    attendance = db.relationship('Attendance', backref='attendance', lazy=True)

    def __repr__(self):
        return f'{self.roll_no}'



class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    roll_no = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def __repr__(self):
        return f'{self.roll_no}, {self.date}'