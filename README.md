# RECOGNITO
Recognito  is a web-based attendance tracking system that uses facial 
recognition to take attendance.

When the students come in front of the camera, their face is matched 
with their photos uploaded by the teachers. Their attendance is marked and 
stored in the database once their face is recognized.

The date and time of attendance are recorded and stored in the database.
The teacher can also download the attendance records of a student or a class as
an excel sheet.


## System Requirements
Make sure that the website has the permission to access the camera and the
camera is not being accessed by some other websites.



## STRUCTURE
`/` or `/home` : Home page for RECOGNITO.

![home-page](https://user-images.githubusercontent.com/78474043/170526300-6e87b063-5897-4417-a2bb-0f88c8feebbe.jpg)

`/login` : A teacher can login himself/herself on the website. 

![login-user-page](https://user-images.githubusercontent.com/78474043/170526593-cbb91784-3b3a-4106-82ec-e37931321005.jpg)

`/register` : A teacher can register himself/herself on the website. 

![register-user-page](https://user-images.githubusercontent.com/78474043/170526629-6c0dc881-e504-4625-84ad-18ed4ec231b3.jpg)

`/profile` : Displays the profile of the teacher (or user). 

![user-profile-page](https://user-images.githubusercontent.com/78474043/170526640-afe38d20-735f-47ca-acb5-9d93041f8875.jpg)

`/register_student` : After logging in, the teacher can register students 
for his/her class. 

![register-student-page](https://user-images.githubusercontent.com/78474043/170526628-c98d9b96-7bfc-489d-9916-6eaf6cf126a1.jpg)

`/upload_photo` : While registering a student, a teacher has to upload the 
picture of the student for sample. 

![upload-photo-page](https://user-images.githubusercontent.com/78474043/170526638-c53ab65d-fa07-4719-95c4-c08848b3461c.jpg)

`/take_attendance` : Attendance for the student is taken via the camera and 
stored in the csv file. Faces are recognized on the basis of photos of the 
students uploaded by the teacher while registering the student.
From the csv file, the attendance records are then stored in the database. 

![take-attendance](https://user-images.githubusercontent.com/78474043/170528435-fea4a48b-76ae-4d42-8fa5-2a009976fcc9.jpg)

`/student_details` : Student details are also displayed on the website with the 
total number of days each student was present in the class. 

![student-details-page](https://user-images.githubusercontent.com/78474043/170526633-f2bf41a6-8c62-420c-b3c4-52085726fa07.jpg)

`/attendance_details` : Here, the teacher is given two choices.
First, the teacher can see all of the attendance of a student.
Or second, the teacher can see the attendance of a class.

![attendance-details-page](https://user-images.githubusercontent.com/78474043/170526662-3db8b8a2-31ca-40e6-90cc-c5a6606d29b1.jpg)

`/enter_roll` : If the teacher chooses to see the attendance of one student then,
he will be directed to this url. Here, he can enter the roll number of the student
of which he wants the attendance to be displayed.

![enter-roll-page](https://user-images.githubusercontent.com/78474043/170526659-dbab8b5f-faf0-43ee-b2cd-34b45122c7e1.jpg)

`/display_by_roll` : Attendance for the student whose roll number was 
previously entered by the teacher will be displayed for all the days he was 
marked present with the date and time of attendance. 
Here, the teacher can also download the attendance as an excel-sheet by clicking
the `Download Attendance` button.

![display-by-roll](https://user-images.githubusercontent.com/78474043/170526653-fad651ba-8d18-47d6-9e76-ef9b6d3f6385.jpg)

`/enter_class` : If the teacher chooses to see the attendance of a class then,
he will be directed to this url. Here, he can enter the department, section, year,
course and teacher name of a class and the date for which he wants the 
attendance to be displayed.

![enter-class](https://user-images.githubusercontent.com/78474043/170526657-3be6d405-0dc1-41a2-a82b-26a917a3202b.jpg)

`/display_by_class` : Attendance for the class whose details were previously 
entered by the teacher will be displayed for the particular date entered.
Here also, the teacher can download the attendance as an excel-sheet by clicking
the `Download Attendance` button. 

![display-by-class](https://user-images.githubusercontent.com/78474043/170526666-c2f4853f-e16b-440f-94b5-c2c882324447.jpg)

`/logout` : Teacher can logout from the website.



## RUN LOCALLY 

Clone the project [Make sure you have git CLI installed]

```bash
  git clone https://github.com/Sneha1203/RECOGNITO.git
```

Go to the project directory.

Make a virtual environment after you have entered the root directory of the project.
```bash
  conda create --name env
  
  #or

  pip -m venv env
```

After making the virtual environment, activate it.
```bash
  conda activate env      # for conda

  env\Scripts\activate        # for pip
```

After activating the virtual environment, install the following dependencies:
```bash
# for conda
  conda install -n env flask
  conda install -n env flask_sqlalchemy
  conda install -n env flask_wtf
  conda install -n env wtforms
  conda install -n env email_validator
  conda install -n env flask_bcrypt
  conda install -n env flask_login
  conda install -n env Pillow
  conda install -n env opencv-python
  conda install -n env opencv-contrib-python
  conda install -n env numpy 
  conda install -n env pandas
  conda install -n env Pillow
  conda install -n env cmake
  conda install -n env dlib
  conda install -n env face-recognition

# for pip
  python -m pip install flask
  python -m pip install flask_sqlalchemy
  python -m pip install flask_wtf
  python -m pip install wtforms
  python -m pip install email_validator
  python -m pip install flask_bcrypt
  python -m pip install flask_login
  python -m pip install Pillow
  python -m pip install opencv-python
  python -m pip install opencv-contrib-python
  python -m pip install numpy 
  python -m pip install pandas
  python -m pip install Pillow
  python -m pip install cmake
  python -m pip install dlib
  python -m pip install face-recognition

```
or you can simply execute

```bash
  conda install --file requirements.txt     # for conda

  pip install -r requirements.txt       # for pip
```


After installing the dependencies, start the server by executing
```bash
  python run.py
```

Open http://localhost:5000/ and verify.