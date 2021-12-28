from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, DepartmentHead, ICT_Professional, Departments, Colleges, Instructor, Course, Students, \
    Attendance, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedBackStudent, FeedBackStaffs, \
    NotificationStudent, NotificationStaffs


# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(Users, UserModel)
admin.site.register(ICT_Professional)
admin.site.register(DepartmentHead)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Colleges)
admin.site.register(Departments)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)
