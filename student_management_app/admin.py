from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student_management_app.models import CustomUser, AdminHOD, Teachers, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportTeacher, FeedBackStudent, FeedBackTeacher, NotificationStudent, NotificationTeacher, StudentSubjectLink


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Teachers)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(StudentSubjectLink)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportTeacher)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackTeacher)
admin.site.register(NotificationStudent)
admin.site.register(NotificationTeacher)
