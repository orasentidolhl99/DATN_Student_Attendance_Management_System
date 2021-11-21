from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime

from student_management_app.models import (
    CustomUser, Teachers, Courses,
    Subjects,Students, SessionYearModel,
    FeedBackStudent, FeedBackTeacher,
    LeaveReportStudent, LeaveReportTeacher,
    Attendance, AttendanceReport,
    StudentSubjectLink
)

from student_management_app.forms import AddStudentForm, EditStudentForm

def admin_home(request):
    return render(request,"admin_template/content_template.html")


# def admin_home(request):
#     all_student_count = Students.objects.all().count()
#     subject_count = Subjects.objects.all().count()
#     course_count = Courses.objects.all().count()
#     teacher_count = Teachers.objects.all().count()

#     # Total Subjects and students in Each Course
#     course_all = Courses.objects.all()
#     course_name_list = []
#     subject_count_list = []
#     student_count_list_in_course = []

#     for course in course_all:
#         subjects = Subjects.objects.filter(course_id=course.id).count()
#         students = Students.objects.filter(course_id=course.id).count()
#         course_name_list.append(course.course_name)
#         subject_count_list.append(subjects)
#         student_count_list_in_course.append(students)
    
#     subject_all = Subjects.objects.all()
#     subject_list = []
#     student_count_list_in_subject = []
#     for subject in subject_all:
#         course = Courses.objects.get(id=subject.course_id.id)
#         student_count = Students.objects.filter(course_id=course.id).count()
#         subject_list.append(subject.subject_name)
#         student_count_list_in_subject.append(student_count)
    
#     # For teacher
#     teacher_attendance_present_list=[]
#     teacher_attendance_leave_list=[]
#     teacher_name_list=[]

#     teachers = Teachers.objects.all()
#     for teacher in teachers:
#         subject_ids = Subjects.objects.filter(teacher_id=teacher.admin.id)
#         attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
#         leaves = LeaveReportTeacher.objects.filter(teacher_id=teacher.id, leave_status=1).count()
#         teacher_attendance_present_list.append(attendance)
#         teacher_attendance_leave_list.append(leaves)
#         teacher_name_list.append(teacher.admin.first_name)

#     # For Students
#     student_attendance_present_list=[]
#     student_attendance_leave_list=[]
#     student_name_list=[]

#     students = Students.objects.all()
#     for student in students:
#         attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
#         absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
#         leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
#         student_attendance_present_list.append(attendance)
#         student_attendance_leave_list.append(leaves+absent)
#         student_name_list.append(student.admin.first_name)


#     context={
#         "all_student_count": all_student_count,
#         "subject_count": subject_count,
#         "course_count": course_count,
#         "teacher_count": teacher_count,
#         "course_name_list": course_name_list,
#         "subject_count_list": subject_count_list,
#         "student_count_list_in_course": student_count_list_in_course,
#         "subject_list": subject_list,
#         "student_count_list_in_subject": student_count_list_in_subject,
#         "teacher_attendance_present_list": teacher_attendance_present_list,
#         "teacher_attendance_leave_list": teacher_attendance_leave_list,
#         "teacher_name_list": teacher_name_list,
#         "student_attendance_present_list": student_attendance_present_list,
#         "student_attendance_leave_list": student_attendance_leave_list,
#         "student_name_list": student_name_list,
#     }
#     return render(request, "admin_template/base_template.html", context)


def add_teacher(request):
    return render(request, "admin_template/add_teacher_template.html")

def add_teacher_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_teacher')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username,
                                                  password=password,
                                                  email=email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  user_type=2)
            user.teachers.address = address
            user.teachers.name = first_name
            user.teachers.email = email
            user.save()
            messages.success(request, "Teacher Added Successfully!")
            return redirect('add_teacher')
        except:
            messages.error(request, "Failed to Add Teacher!")
            return redirect('add_teacher')
            
def manage_teacher(request):
    teachers = Teachers.objects.all()
    context = {
        "teachers": teachers
    }
    return render(request, "admin_template/manage_teacher_template.html", context)

def edit_teacher(request, teacher_id):
    try:
        teacher = Teachers.objects.get(admin=teacher_id)
        if not teacher:
            messages.error(request, f"Teacher not found!")
            return redirect('manage_teacher')
    except:
        messages.error(request, f"Failed to edit Teacher!")
        return redirect('manage_teacher')
    context = {
        "teacher": teacher,
        "id": teacher_id
    }
    return render(request, "admin_template/edit_teacher_template.html", context)

def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id = request.POST.get('teacher_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into teacher Model
            teacher_model = Teachers.objects.get(admin=teacher_id)
            teacher_model.address = address
            teacher_model.updated_at = datetime.now()
            teacher_model.save()

            messages.success(request, "Teacher Updated Successfully.")
            # return redirect('/edit_teacher/'+teacher_id)
            return redirect('manage_teacher')

        except:
            messages.error(request, "Failed to Update Teacher.")
            # return redirect('/edit_teacher/'+teacher_id)
            return redirect('manage_teacher')

def delete_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    try:
        teacher.delete()
        teacher.admin.delete()
        messages.success(request, "Teacher Deleted Successfully.")
        return redirect('manage_teacher')
    except:
        messages.error(request, "Failed to Delete Teacher.")
        return redirect('manage_teacher')

# not yet
def add_student_subject_link(request, subject_id):
    subjects = Subjects.objects.get(id=subject_id)
    students = Students.objects.filter(course_id=subjects.course_id)

    student_subject_link = [
        student.student_id for student in StudentSubjectLink.objects\
            .filter(subject_id=subjects)
    ]
    get_students_others = [
        student for student in students if student not in student_subject_link
    ]

    context = {
        'subjects': subjects,
        'students': get_students_others
    }
    return render(request, "admin_template/add_student_subject_link.html", context=context)

# not yet
def add_student_subject_link_save(request, subject_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_student_subject_link', subject_id)
    else:
        student_id = request.POST.get('student_id')
        
        subject = Subjects.objects.get(id=subject_id)
        student = Students.objects.get(id=student_id)
        
        print(f"student_id = {student_id}, subject_id = {subject_id}")
        try:
            student_subject = StudentSubjectLink.objects.create(student_id=student, subject_id=subject)
            student_subject.save()
            messages.success(request, "Student Subject Added Successfully!")
            return redirect('manage_student_subject_link', subject_id)
        except:
            messages.error(request, "Failed to Add Student Subject!")
            return redirect('add_student_subject_link_save', subject_id)
        
def manage_student_subject_link(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    student_subject_link = StudentSubjectLink.objects.filter(subject_id=subject)
    context = {
        'subject': subject,
        'student_subject_link': student_subject_link
    }
    return render(request,"admin_template/manage_student_subject_link_template.html", context=context)


def delete_student_subject_link(request, student_subject_id):
    student_subject_link = StudentSubjectLink.objects.get(id=student_subject_id)
    subject_id = student_subject_link.subject_id.id
    try:
        student_subject_link.delete()
        messages.success(request, "Student Subject Deleted Successfully.")
        return redirect('manage_student_subject_link', subject_id)
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_student_subject_link', subject_id)


def add_course(request):
    return render(request,"admin_template/add_course_template.html")

def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        if not course:
            messages.error(request, f"Please enter course!")
            return redirect('add_course')
        
        try:
            check_course = Courses.objects.filter(course_name=course)
            if check_course:
                messages.error(request, f"Course \"{course}\" is really existing!")
                return redirect('add_course')
            
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, f"Course \"{course}\" added successfully.")
            return redirect('add_course')   
        except:
            messages.error(request, f"Failed to Add Course \"{course}\"!")
            return redirect('add_course')

def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'admin_template/manage_course_template.html', context)

def edit_course(request, course_id):
    try:
        course = Courses.objects.get(id=course_id)
        if not course:
            messages.error(request, f"Course not found!")
            return redirect('manage_course')
    except:
        messages.error(request, f"Failed to edit Course!")
        return redirect('manage_course')
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'admin_template/edit_course_template.html', context)

def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')
        if not course_name:
            messages.error(request, f"Please enter course!")
            return redirect('/edit_course/' + course_id)
        
        try:
            course = Courses.objects.get(id=course_id)
            if str(course.course_name) == str(course_name):
                messages.error(request, f"Course \"{course_name}\" is really existing!")
                return redirect('/edit_course/' + course_id)
            
            course.course_name = course_name
            course.updated_at = datetime.now()
            course.save()
            messages.success(request, f"Course \"{course_name}\" updated successfully.")
            # return redirect('/edit_course/' + course_id)
            return redirect('manage_course')

        except:
            messages.error(request, "Failed to Update Course.")
            # return redirect('/edit_course/' + course_id)
            return redirect('manage_course')
        
def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    course_name = course.course_name
    try:
        course.delete()
        messages.success(request, f"Course \"{course_name}\" deleted successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


def add_session(request):
    return render(request, "admin_template/add_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")

def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "admin_template/manage_session_template.html", context)

def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "admin_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.updated_at = datetime.now()
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'admin_template/add_student_template.html', context)

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj

                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')

def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'admin_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)

    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['course_id'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "admin_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                if int(course_id) != int(student_model.course_id.id):
                    # delete the student in subject - course old
                    all_student = StudentSubjectLink.objects.filter(student_id=student_model)
                    for student in all_student:
                        student.delete()
                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                    
                student_model.updated_at = datetime.now()
                
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    courses = Courses.objects.all()
    teachers = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "teachers": teachers
    }
    return render(request,"admin_template/add_subject_template.html", context)

def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        
        teacher_id = request.POST.get('teacher')
        teacher = CustomUser.objects.get(id=teacher_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, teacher_id=teacher)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            # return redirect('add_subject')
            return redirect('/manage_subject/')
        except:
            messages.error(request, "Failed to Add Subject!")
            # return redirect('add_subject')
            return redirect('/manage_subject/')

def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'admin_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    
    try:
        subject = Subjects.objects.get(id=subject_id)
        courses = Courses.objects.all()
        teachers = CustomUser.objects.filter(user_type='2')
        if not subject:
            messages.error(request, f"Subject not found!")
            return redirect('manage_subject')
    except:
        messages.error(request, f"Failed to edit Subject!")
        return redirect('manage_subject')
    context = {
        "subject": subject,
        "courses": courses,
        "teachers": teachers,
        "id": subject_id
    }
    return render(request, 'admin_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        
        if not subject_name:
            messages.error(request, f"Please enter subject!")
            return redirect('/edit_subject/' + subject_id)

        try:
            subject = Subjects.objects.get(id=subject_id)
            course = Courses.objects.get(id=course_id)
            teacher = CustomUser.objects.get(id=teacher_id)
            
            check_subject_exist = Subjects.objects\
                .filter(subject_name=str(subject_name),
                        course_id=course, teacher_id=teacher)
            
            if check_subject_exist:
                messages.error(request, f"Subject \"{subject_name}\" is really existing!")
                return redirect('/edit_subject/' + subject_id)
            
            subject.subject_name = subject_name
            subject.course_id = course
            subject.teacher_id = teacher
            subject.updated_at = datetime.now()
            
            subject.save()
            messages.success(request, "Subject Updated Successfully.")
            # return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            return redirect('/manage_subject/')

        except:
            messages.error(request, "Failed to Update Subject.")
            # return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            return redirect('/manage_subject/')



def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def teacher_feedback_message(request):
    feedbacks = FeedBackTeacher.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_template/teacher_feedback_template.html', context)


@csrf_exempt
def teacher_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackTeacher.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


# def student_leave_view(request):
#     leaves = LeaveReportStudent.objects.all()
#     context = {
#         "leaves": leaves
#     }
#     return render(request, 'admin_template/student_leave_view.html', context)

# def student_leave_approve(request, leave_id):
#     leave = LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status = 1
#     leave.save()
#     return redirect('student_leave_view')


# def student_leave_reject(request, leave_id):
#     leave = LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status = 2
#     leave.save()
#     return redirect('student_leave_view')


def teacher_leave_view(request):
    leaves = LeaveReportTeacher.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'admin_template/teacher_leave_view.html', context)


def teacher_leave_approve(request, leave_id):
    leave = LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('teacher_leave_view')


def teacher_leave_reject(request, leave_id):
    leave = LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('teacher_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "admin_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
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
def admin_get_attendance_student(request):
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


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admin_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def teacher_profile(request):
    pass


def student_profile(request):
    pass
