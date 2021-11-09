from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from student_management_app.models import CustomUser, Teachers, Courses, Subjects, Students


def admin_home(request):
    return render(request, "hod_template/base_template.html")

def add_teacher(request):
    return render(request, "hod_template/add_teacher_template.html")

def add_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.teachers.address = address
            user.save()
            messages.success(request, "Teacher Added Successfully!")
            return HttpResponseRedirect('add_teacher')
        except:
            messages.error(request, "Failed to Add Teacher!")
            return HttpResponseRedirect('add_teacher')
def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get('course')
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    courses = Courses.objects.all()
    return render(request,'hod_template/add_student_template.html', {"courses": courses})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        course_id = request.POST.get('course')
        gender = request.POST.get('gender')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.session_start_year = start_date
            user.students.session_end_year = end_date
            user.students.gender = gender
            user.students.profile_pic = ""
            user.save()
            messages.success(request, "Student Added Successfully!")
            return HttpResponseRedirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return HttpResponseRedirect('add_student')

def add_subject(request):
    courses = Courses.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    context = {
        "courses": courses,
        "teachers": teachers
    }
    return render(request,"hod_template/add_subject_template.html", context)

def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)        
        teacher_id = request.POST.get('teacher')
        teacher = CustomUser.objects.get(id = teacher_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, teacher_id=teacher)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return HttpResponseRedirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return HttpResponseRedirect('add_subject')

def manage_teacher(request):
    teachers = Teachers.objects.all()
    return render(request,'hod_template/manage_teacher_template.html',{"teachers": teachers})

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student_template.html', {"students": students})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request,'hod_template/manage_course_template.html',{"courses": courses})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request,'hod_template/manage_subject_template.html',{"subjects": subjects})