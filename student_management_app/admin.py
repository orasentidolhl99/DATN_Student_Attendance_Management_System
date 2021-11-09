from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser, AdminHOD, Courses, Teachers, Students


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(AdminHOD)
admin.site.register(Courses)
admin.site.register(Teachers)
admin.site.register(Students)
