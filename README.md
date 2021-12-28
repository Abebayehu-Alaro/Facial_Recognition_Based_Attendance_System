# Facial Recognition based Attendance System
Facial Recognition Based Attendance System is a machine learning-based system that handles and 
tracks the student attendance system using the web application and deep learning 
algorithms/models.

And if you like this project then ADD a STAR ⭐️  to this project 👆

## Features of this Project

The proposed system is expected to provide student attendance system-related functionalities 
like marking attendance using face recognition and making the report for the recorded 
attendance. For a better understanding of our system, we divided the functionalities of our 
system by modules. The proposed system is expected to provide the following services.
### Admin Module / Super Administrator
1. The system shall allow the admin to enter all the new users’ (students, lecturers, 
department heads, and admins) information. 
2. The system shall allow the admin to delete the users(student/s, lecturer/s, department 
head/s, and admin/s) that ceased their enrollment in the attendance workflow. 
3. The system shall allow the admin to add the departments and colleges.
4. The system shall allow the admin to delete the departments and colleges.
5. The system shall allow the admin to give the role for the lecturer as department 
administrator or department head.
6. The system shall allow the admin to upload the new students' images in order to 
preprocess them and store them on the database.
7. The system shall allow the admin to train the model on the newly uploaded images of 
students.
8. The system shall allow the admin to initialize the attendance system by configuring the 
basic attendance settings like Late Time (Mins), Beginning/Ending In Time, etc.
9. The system shall allow the admin to view the attendance tracking status of the system.
10. The system shall allow the admin to log into and log out from the system.
11. The system shall enable the admin to update their profiles.
###Student Module
1. The system shall allow the students to view their attendance status of the specific course.
2. The system shall allow the students to log into and log out from the system.
3. The system shall enable the students to update their profiles.
###The Department Head Module / Department Administrator
1. The system should allow the Head to view his/her students’ attendance status.
2. The system should allow the Head to register courses’ information.
3. The system should allow the Head to register students for the specific courses.
4. The system should allow the Head to assign an instructor to a course/courses that he/she 
is going to instruct and control the attendance tracking.
5. The system should allow the Head to delete the assigned instructor to a course or courses 
due to the special case that made the instructor cease instructing that course/courses.
6. The system should allow the Head to set up the attendance rule for the specific course.
7. The system should allow the Head to set up the schedule for the specific course.
8. The system shall allow the Head to log into and log out from the system.
9. The system shall enable the Head to update his/her profile.
###Instructor Module
1. The system shall allow the Academic Staff to configure the basic settings for the 
attendance that is going to be taken.
2. The system shall allow the Academic Staff to initiate the attendance tracking of the 
specific section.
3. The system shall allow the Academic Staff to cease the attendance tracking of the 
specific section.
4. The system shall allow the Academic Staff to view the attendance status of students that 
he/she instructs.
5. The system shall allow the Academic Staff to handle the special case attendance of 
students.
6. The system shall allow the Academic Staff to log into and log out from the system.
7. The system shall enable the Head to update his/her profile.
###Report Module
1. The system shall generate the Daily Attendance Statistical Report that lists the definite 
section daily attendance status for the specific course in the assigned time in the table.
Viewers: Instructor, Head of the Department, and Admin
2. The system shall generate an Attendance General Report that is used to show the sum 
computation of the definite section individual student attendance statistical status for the 
specific course in the assigned time.
Viewers: Head of the Department, and Admin
3. The system shall generate the Department Attendance Statistical Report that shows the 
sum total of all students' attendance status of the specific department in the assigned time.
Viewer: Admin
4. The system shall generate the specific student attendance report that shows the specific 
student attendance status of the specific course in the assigned time.
Viewer: Student
5. The system shall generate the final taking student list for the specific course.
Viewers: Instructor, Head of the Department, and Admin
6. The system shall generate for the special purpose recorded student attendance list.
Viewers: Instructor, Head of the Department, and Admin


## Support Developer
1. Subscribe & Share my YouTube Channel - https://www.youtube.com/channel/UCq8hiPvoziDcrboY6UEGkIg
2. Add a Star 🌟  to this 👆 Repository



## How to Install and Run this project?

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]

*Alternative to Pip is Homebrew*

### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Mac
```
$  source venv/bin/activate
```
3. Install tensorflow, keras, mysqlclient, mtcnn, and all necessary ai and django related libraries.

**4. Clone this project**
```
$  git clone https://github.com/vijaythapa333/django-student-management-system.git
```

Then, Enter the project
```
$  cd django-student-management-system
```

**5. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```

**6. Add the hosts**

- Got to settings.py file 
- Then, On allowed hosts, Add [‘*’]. 
```python
ALLOWED_HOSTS = ['*']
```
*No need to change on Mac.*


**6. Now Run Server**

Command for PC:
```python
$ python manage.py runserver
```

Command for Mac:
```python
$ python3 manage.py runserver
```

**7. Login Credentials**

Create Super User (Admin)
```
$  python manage.py createsuperuser
```
Then Add Email, Username and Password


## For Sponsor or Projects Enquiry
1. Email - abebayehualaro1@gmail.com
2. LinkedIn - [Abebayehu Alaro](https://www.linkedin.com/in/abebayehu-alaro/ "Abebayehu Alaro on LinkedIn")

