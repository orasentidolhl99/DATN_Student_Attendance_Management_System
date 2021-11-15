from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import CustomUser, Courses, SessionYearModel
from student_management_system import settings

import datetime
import json
import os


# Create your views here.
def ShowDemoPage(request):
    return render(request,"demo.html")

def loginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Teacher Login")
                return redirect('teacher_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user!=None:
        return HttpResponse("User :" + request.user.email+" Usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First!")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def delete(request):
    pass 