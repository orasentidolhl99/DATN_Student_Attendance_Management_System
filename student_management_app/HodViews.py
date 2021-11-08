from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import CustomUser


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
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    return render(request,'hod_template/add_student_template.html')

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

            start_date = datetime.datetime.strptime(session_start, '%d-%m-%y').strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(session_end, '%d-%m-%y').strftime('%Y-%m-%d')



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