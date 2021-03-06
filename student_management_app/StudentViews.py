from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
import datetime  # To Parse input DateTime into Python Date Time Object

from student_management_app.models import Users, Instructor, Course, Students, \
    LeaveReportStudent, FeedBackStudent, \
    RegisterForCourse, DepartmentHead, ICT_Professional, AssignInstructor, AttendanceReport, Attendance


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    # course_obj = Courses.objects.get(id=student_obj.course_id.id)
    subjects = RegisterForCourse.objects.filter(student_id=student_obj)
    total_subjects = RegisterForCourse.objects.filter(student_id=student_obj).count()
    subject_data = []
    for subject in subjects:
        subject_data.append(subject.subject_id)
    subject_name = []
    data_present = []
    data_absent = []
    # subject_data = Course.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                     student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,
                                                                    student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    context = {
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)  # Getting Logged in Student Data
    # course = student.course_id  # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    attendances = AttendanceReport.objects.filter(student_id=student)
    subjects = []
    for attendance in attendances:
        if attendance.attendance_id.subject_id not in subjects:
            subjects.append(attendance.attendance_id.subject_id)
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Course.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = Users.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                                 subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)


def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    # Receiver
    head = DepartmentHead.objects.get(department_id=student_obj.department_id)
    object_list = RegisterForCourse.objects.filter(student_id=student_obj)
    objects_list = []
    staffs_list = []
    for obj in object_list:
        objects_list.append(AssignInstructor.objects.filter(subject_id=obj.subject_id))
    for objs in objects_list:
        for obj in objs:
            if obj.staff_id not in staffs_list:
                staffs_list.append(obj.staff_id)
    # objects_list = []
    # for obj in object_list:
    #     objects_list.append(AssignInstructor.objects.get(subject_id=obj.subject_id))
    context = {
        "leave_data": leave_data,
        # "subjects": objects_list,
        "staffs": staffs_list,
        'head': head,
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        receiver = request.POST.get('receiver')

        student_obj = Students.objects.get(admin=request.user.id)
        staff = Instructor.objects.get(id=receiver)
        receiver_obj = Users.objects.get(id=staff.admin.id)
        try:
            leave_report = LeaveReportStudent(receiver=receiver_obj, student_id=student_obj, leave_date=leave_date,
                                              leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    # Receiver
    admin = ICT_Professional.objects.all()
    head = DepartmentHead.objects.get(department_id=student_obj.department_id)
    object_list = RegisterForCourse.objects.filter(student_id=student_obj)
    objects_list = []
    for obj in object_list:
        objects_list.append(AssignInstructor.objects.filter(subject_id=obj.subject_id))
    staffs_list = []
    for objs in objects_list:
        for obj in objs:
            if obj.staff_id not in staffs_list:
                staffs_list.append(obj.staff_id)
    context = {
        "feedback_data": feedback_data,
        "admins": admin,
        "head": head,
        # "subjects": objects_list,
        "staffs": staffs_list,
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)
        receiver = request.POST.get('receiver')

        receiver_obj = Users.objects.get(id=receiver)
        try:
            add_feedback = FeedBackStudent(receiver=receiver_obj, student_id=student_obj, feedback=feedback,
                                           feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = Users.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    context = {
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_base(request):
    user = Users.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    context = {
        "user": user,
        "student": student
    }
    return render(request, 'student_template/sidebar_template.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = Users.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')
