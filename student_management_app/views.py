from django.contrib.auth import authenticate,login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages

# Create your views here.
def ShowDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            return HttpResponseRedirect('/admin_home')
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User :" + request.user.email+" Usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First!")

def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect("/")