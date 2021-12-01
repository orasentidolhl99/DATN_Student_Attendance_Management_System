from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent, NotificationStudent, StudentResult, SessionYearModel, StudentSubjectLink

def student_home(request):
    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    context={
        "user": user,
        "student": student
    }
    return render(request, "student_template/student_home_template.html",context)

# def student_home(request):
#     student_obj = Students.objects.get(admin=request.user.id)
#     total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
#     attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
#     attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

#     course_obj = Courses.objects.get(id=student_obj.course_id.id)
#     total_subjects = Subjects.objects.filter(course_id=course_obj).count()

#     subject_name = []
#     data_present = []
#     data_absent = []
#     subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
#     for subject in subject_data:
#         attendance = Attendance.objects.filter(subject_id=subject.id)
#         attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
#         attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
#         subject_name.append(subject.subject_name)
#         data_present.append(attendance_present_count)
#         data_absent.append(attendance_absent_count)
    
#     context={
#         "total_attendance": total_attendance,
#         "attendance_present": attendance_present,
#         "attendance_absent": attendance_absent,
#         "total_subjects": total_subjects,
#         "subject_name": subject_name,
#         "data_present": data_present,
#         "data_absent": data_absent
#     }
#     return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    course = student.course_id # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects,
        "user": user,
        "student": student
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    # Getting all the Input Data
    subject_id = request.POST.get('subject')

    start_date = request.POST.get('start_date')
    if start_date == "":
        messages.error(request, "Please choose start date!")
        return redirect('student_view_attendance')

    end_date = request.POST.get('end_date')
    if end_date == "":
        messages.error(request, "Please choose end date!")
        return redirect('student_view_attendance')

    # Parsing the date data into Python object
    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Getting all the Subject Data based on Selected Subject
    subject_obj = Subjects.objects.get(id=subject_id)
    # Getting Logged In User Data
    user_obj = CustomUser.objects.get(id=request.user.id)
    # Getting Student Data Based on Logged in Data
    stud_obj = Students.objects.get(admin=user_obj)

    # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
    # Getting Attendance Report based on the attendance details obtained above
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

    # for attendance_report in attendance_reports:
    #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

    # messages.success(request, "Attendacne View Success")

    context = {
        "subject_obj": subject_obj,
        "attendance_reports": attendance_reports,
        "user": user,
        "student": student
    }

    return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):

    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    student_obj = Students.objects.get(admin=request.user.id)
    subjects = StudentSubjectLink.objects.filter(student_id=student_obj)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "subjects": subjects,
        "leave_data": leave_data,
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        if leave_date == "":
            messages.error(request, "Please choose leave date!")
            return redirect('student_apply_leave')

        leave_message = request.POST.get('leave_message')
        if leave_message == "":
            messages.error(request, "Please enter leave message!")
            return redirect('student_apply_leave')

        leave_subject = request.POST.get('leave_subject')
        
        student_obj = Students.objects.get(admin=request.user.id)
        subject_obj = StudentSubjectLink.objects.get(id=leave_subject)
        
        try:
            leave_report = LeaveReportStudent(student_id=student_obj,
                                              subject_id=subject_obj.subject_id,
                                              leave_date=leave_date,
                                              leave_message=leave_message,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):

    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data,
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        if feedback == "":
            messages.error(request, "Please enter feedback message!")
            return redirect('student_feedback')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    context={
        "user": user,
        "student": student
    }
    return render(request, "student_template/student_profile.html", context)

def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get('first_name')
        if first_name == "":
            messages.error(request, "Please enter first name!")
            return redirect('student_profile')

        last_name = request.POST.get('last_name')
        if last_name == "":
            messages.error(request, "Please enter last name!")
            return redirect('student_profile')

        address = request.POST.get('address')
        if address == "":
            messages.error(request, "Please enter address!")
            return redirect('student_profile')

        password = request.POST.get('password')
        # if password == "":
        #     messages.error(request, "Please enter password!")
        #     return redirect('student_profile')

        try:
            custom_user = CustomUser.objects.get(id = request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password is not None and password != "":
                custom_user.set_password(password)
            custom_user.save()

            student = Students.objects.get(admin=custom_user)
            student.address = address
            student.save()
            
            if password == "":
                messages.success(request, "Profile Updated Successfully")
                return redirect('student_profile')
            else:
                messages.success(request, "Password has been changed, sign in again!")
                return redirect('logout_user')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):

    # Show image profile
    user = CustomUser.objects.get(id = request.user.id)
    student = Students.objects.get(admin = user)

    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
        "user": user,
        "student": student
    }
    return render(request, "student_template/student_view_result.html", context)





