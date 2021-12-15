from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime
# import unidecode

from django.http.response import StreamingHttpResponse

# common settings
from ..camera import FaceDetect
from ..utils import datetime_counter

from student_management_app.models import (
    CustomUser, Teachers, Courses, Subjects,
    Students, SessionYearModel, Attendance, 
    AttendanceReport, LeaveReportTeacher,
    FeedBackTeacher, StudentResult,
    LeaveReportStudent, StudentSubjectLink
)

def teacher_home(request):
    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)
    # Fetching All Students under teacher

    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    students_count = Students.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    teacher = Teachers.objects.get(admin=request.user.id)
    leave_count = LeaveReportTeacher.objects.filter(teacher_id=teacher.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)

    context={
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent,

        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
        
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/teacher_home_template.html", context)

def teacher_take_attendance(request):

    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)

    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/take_attendance_template.html", context)

@csrf_exempt
def take_attendance_detect(request):
    subject_id = request.GET.get('subject_id')
    session_year_id = request.GET.get('session_year_id')
    
    subject_model = Subjects.objects.get(id=subject_id)
    
    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)

    context = {
        "subjects":subject_model,
        "session_year_id": session_year_id,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/take_attendance_detect.html",context)

dict_check = dict()

def gen(camera):
    while True:
        frame, student_info = camera.get_frame()

        if student_info:
            list_unique_ids = dict_check.keys()

            if int(student_info['student_code']) not in list_unique_ids:
                dict_check[int(student_info['student_code'])] = []
            else:
                dict_check[int(student_info['student_code'])].append(student_info['check_time'])
                
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def facecam_feed(request):
    # init data detect
    dict_check.clear()
    # take frame video stream from client
    return StreamingHttpResponse(gen(FaceDetect()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def attendance_result_stream(request):
    subject_id = request.GET.get('subject_id')
    session_year_id = request.GET.get('session_year_id')
    
    # subject = Subjects.objects.get(id=subject_id)
    # student_subject_link = StudentSubjectLink.objects.filter(subject_id=subject)
    
    # for student in student_subject_link:
    #     print(student.student_id.admin.username)
    
    subjects = Subjects.objects.get(id=subject_id)
    # students = Students.objects.filter(course_id=subjects.course_id)

    student_subject_link = [
        {
            "student_id": str(student.student_id.admin.username),
            "full_name": f"{student.student_id.admin.last_name} { student.student_id.admin.first_name }",
            "time_in_class": "",
            "status":""
        } for student in StudentSubjectLink.objects\
            .filter(subject_id=subjects)
    ]
    
    # print(student_subject_link)
    
    list_obj = datetime_counter(dict_check)
    # print(list_obj)
        
    list_result = []
    
    for item in student_subject_link:
        if item["student_id"] in list_obj.keys():
            if  int(list_obj[item["student_id"]]['counter']) > 3:
                time_in_class = datetime.strptime(list_obj[item["student_id"]]['datetime'], "%m-%d-%Y, %H:%M:%S")
                
                print("+++++++++++++" + item["student_id"])
                # print(list_obj[item["student_id"]])
                
                list_result.append(
                    {
                        "student_id": item["student_id"],
                        "full_name": item["full_name"],
                        "time_in_class": time_in_class,
                        "status": "checked"
                    }
                )
                
            else:
                time_in_class = ""
            
                print("-------------" + item["student_id"])
                # print(list_obj[item["student_id"]])
                
                list_result.append(
                    {
                        "student_id": item["student_id"],
                        "full_name": item["full_name"],
                        "time_in_class": time_in_class,
                        "status": ""
                    }
                )
                
        else:
            time_in_class = ""
            
            print("-------------" + item["student_id"])
            # print(list_obj[item["student_id"]])
            
            list_result.append(
                {
                    "student_id": item["student_id"],
                    "full_name": item["full_name"],
                    "time_in_class": time_in_class,
                    "status": ""
                }
            )
            
    # list_result = []

    # for obj_student in list_obj:
    #     if int(obj_student['counter']) > 3:
    #         time_in_class = datetime.strptime(obj_student['datetime'], "%m-%d-%Y, %H:%M:%S")
    #     else:
    #         time_in_class = None
        
    #     list_result.append(
    #         {
    #             "student_id": str(obj_student['student_id']),
    #             "time_in_class": time_in_class,
    #             "status": "Absent" if time_in_class is None else "checked"
    #         }
    #     )
    # print(list_ids_student_subject)
    context = {
        "subject_id": subject_id,
        "session_year_id": session_year_id,
        "students": list_obj,
        "result_stream": list_result
    }
    return render(request, "teacher_template/attendance_result_stream.html", context=context)


def save_detect_attendance_data(request):
    if request.method == 'POST':
        subject_id = request.GET.get('subject_id')
        session_year_id = request.GET.get('session_year_id')
        
        subject_model = Subjects.objects.get(id=subject_id)
        print(subject_model.subject_name)
        session_year_model = SessionYearModel.objects.get(id=session_year_id)
        print(session_year_model.session_start_year)
        
        attendance_date = datetime.now()
        print(attendance_date)
        
        student_ids = request.POST.getlist('status')
        for student in student_ids:
            print(">>>>>" + student)
        
        student_subject_link = [
            {
                "student_id": str(student.student_id.admin.username),
                "status": ""
            } for student in StudentSubjectLink.objects\
                .filter(subject_id=subject_model)
        ]                       
        
        list_result = []
        for item in student_subject_link:
            if item["student_id"] in student_ids:
                print("+++++++++++++" + item["student_id"])
                list_result.append(
                    {
                        "student_id": str(item["student_id"]),
                        "status": 1
                    }
                )
            else:
                print("-------------" + item["student_id"])
                list_result.append(
                    {
                        "student_id": str(item["student_id"]),
                        "status": 0
                    }
                )
        print(list_result)
        try:
            # First Attendance Data is Saved on Attendance Model
            attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
            attendance.save()

            for stud in list_result:
                # Attendance of Individual Student saved on AttendanceReport Model
                user = CustomUser.objects.get(username = stud["student_id"])
                student = Students.objects.get(admin=user)
                attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud["status"])
                attendance_report.save()
            return HttpResponse("OK")
        except:
            return HttpResponse("Error")
        
    return redirect('teacher_home')


@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.last_name+" "+student.admin.first_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def teacher_update_attendance(request):
    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)

    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def teacher_apply_leave(request):

    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)

    teacher_obj = Teachers.objects.get(admin=request.user.id)
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    leave_data = LeaveReportTeacher.objects.filter(teacher_id=teacher_obj)
    context = {
        "subjects": subjects,
        "leave_data": leave_data,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/teacher_apply_leave_template.html", context)

def teacher_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_apply_leave')
    else:
        
        leave_date = request.POST.get('leave_date')
        if leave_date == "":
            messages.error(request, "Please choose leave date!")
            return redirect('teacher_apply_leave') 
        

        leave_message = request.POST.get('leave_message')
        if leave_message == "":
            messages.error(request, "Please enter leave message!")
            return redirect('teacher_apply_leave')

        leave_subject = request.POST.get('leave_subject')
        
        teacher_obj = Teachers.objects.get(admin=request.user.id)
        subject_obj = Subjects.objects.get(id=leave_subject)
        try:
            leave_report = LeaveReportTeacher(teacher_id=teacher_obj,
                                              subject_id=subject_obj,
                                              leave_date=leave_date,
                                              leave_message=leave_message,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('teacher_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('teacher_apply_leave')

def teacher_feedback(request):

    user = CustomUser.objects.get(id = request.user.id)
    teacher = Teachers.objects.get(admin = user)

    teacher_obj = Teachers.objects.get(admin=request.user.id)
    feedback_data = FeedBackTeacher.objects.filter(teacher_id=teacher_obj)
    context = {
        "feedback_data":feedback_data,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/teacher_feedback_template.html", context)

def teacher_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('teacher_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        if feedback == "":
            messages.error(request, "Please enter feedback message!")
            return redirect('teacher_feedback')
        teacher_obj = Teachers.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackTeacher(teacher_id=teacher_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('teacher_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('teacher_feedback')

def teacher_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)
    
    context={
        "user": user,
        "teacher": teacher
    }
    return render(request, 'teacher_template/teacher_profile.html', context)

# def teacher_profile_save(request):
    # if request.method!="POST":
    #     return HttpResponseRedirect(reverse("teacher_profile"))
    # else:
    #     first_name = request.POST.get("first_name")
    #     if first_name == "":
    #         messages.error(request, "Please enter first name!")
    #         return redirect('teacher_profile')

    #     last_name = request.POST.get("last_name")
    #     if last_name == "":
    #         messages.error(request, "Please enter last name!")
    #         return redirect('teacher_profile')

    #     address = request.POST.get("address")
    #     if address == "":
    #         messages.error(request, "Please enter address!")
    #         return redirect('teacher_profile')

    #     password = request.POST.get("password")
    #     if password == "":
    #         messages.error(request, "Please enter password!")
    #         return redirect('teacher_profile')

    #     try:
    #         customuser = CustomUser.objects.get(id = request.user.id)
    #         customuser.first_name = first_name
    #         customuser.last_name = last_name
    #         if password!= None and password!= "":
    #             customuser.set_password(password)
    #         customuser.save()

    #         teacher=Teachers.objects.get(admin=customuser.id)
    #         teacher.address=address
    #         teacher.save()
    #         messages.success(request, "Successfully Updated Profile")
    #         return HttpResponseRedirect(reverse("teacher_profile"))
    #     except:
    #         messages.error(request, "Failed to Update Profile")
    #         return HttpResponseRedirect(reverse("teacher_profile"))

def teacher_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('teacher_profile')
    else:
        first_name = request.POST.get('first_name')
        if first_name == "":
            messages.error(request, "Please enter first name!")
            return redirect('teacher_profile')
        
        last_name = request.POST.get('last_name')
        if last_name == "":
            messages.error(request, "Please enter last name!")
            return redirect('teacher_profile')
        
        address = request.POST.get('address')
        if address == "":
            messages.error(request, "Please enter address!")
            return redirect('teacher_profile')
        
        password = request.POST.get('password')
        # if password == "":
        #     messages.error(request, "Please enter password!")
        #     return redirect('teacher_profile')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            customuser.save()

            teacher = Teachers.objects.get(admin=customuser.id)
            teacher.address = address
            teacher.save()
            if password == "":
                messages.success(request, "Profile Updated Successfully")
                return redirect('teacher_profile')
            else:
                messages.success(request, "Password has been changed, sign in again!")
                return redirect('logout_user')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('teacher_profile')

def student_leave_view(request):

    user = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)

    # find all subject 
    all_subjects_in_teacher = Subjects.objects.filter(teacher_id=request.user.id)
    leaves = LeaveReportStudent.objects.filter(subject_id__in=all_subjects_in_teacher)
    context = {
        "leaves": leaves,
        "user": user,
        "teacher": teacher
    }
    return render(request, 'teacher_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')

def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')

def teacher_add_result(request):

    user = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)

    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years,
        "user": user,
        "teacher": teacher
    }
    return render(request, "teacher_template/add_result_template.html", context)


def teacher_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                # return redirect('teacher_add_result')
                return HttpResponseRedirect(reverse("teacher_add_result"))
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                # return redirect('teacher_add_result')
                return HttpResponseRedirect(reverse("teacher_add_result"))
        except:
            messages.error(request, "Failed to Add Result!")
            # return redirect('teacher_add_result')
            return HttpResponseRedirect(reverse("teacher_add_result"))

@csrf_exempt
def fetch_result_student(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")