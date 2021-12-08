from django import forms 
from django.forms import ChoiceField
from student_management_app.models import Courses, SessionYearModel, Subjects, Students

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass
class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Student ID", max_length=50, widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address = forms.CharField(label="Address", max_length=255, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    course_id = forms.ModelChoiceField(
        empty_label=None, label="Course",
        queryset=Courses.objects.all().order_by('id'),
        to_field_name='id',
        widget=forms.Select(attrs={"class":"form-control"})
    )
    
    session_year_id = forms.ModelChoiceField(
        empty_label=None, label="Session Year",
        queryset=SessionYearModel.objects.all().order_by('id'),
        to_field_name='id',
        widget=forms.Select(attrs={"class":"form-control"})
    )
    
    # #For Displaying Courses
    # try:
    #     courses = Courses.objects.all()
    #     course_list = []
    #     for course in courses:
    #         single_course = (course.id, course.course_name)
    #         course_list.append(single_course)
    # except:
    #     course_list = []

    #For Displaying Session Years

    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)
    # except:
    #     session_year_list = []

    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    # course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=255, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Student ID", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=255, widget=forms.TextInput(attrs={"class":"form-control"}))
    

    course_id = forms.ModelChoiceField(
        empty_label=None, label="Course",
        queryset=Courses.objects.all().order_by('id'),
        to_field_name='id',
        widget=forms.Select(attrs={"class":"form-control"})
    )
    
    session_year_id = forms.ModelChoiceField(
        empty_label=None, label="Session Year",
        queryset=SessionYearModel.objects.all().order_by('id'),
        to_field_name='id',
        widget=forms.Select(attrs={"class":"form-control"})
    )

    # #For Displaying Courses
    # course_list = []
    # try:
    #     courses = Courses.objects.all()
    #     for course in courses:
    #         single_course = (course.id, course.course_name)
    #         course_list.append(single_course)
    # except:
    #     course_list = []

    # #For Displaying Session Years
    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)
    # except:
    #     session_year_list = []

    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    # course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    
class EditResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.teacher_id=kwargs.pop("teacher_id")
        super(EditResultForm,self).__init__(*args,**kwargs)
        subject_list=[]
        try:
            subjects=Subjects.objects.filter(teacher_id=self.teacher_id)
            for subject in subjects:
                subject_single=(subject.id,subject.subject_name)
                subject_list.append(subject_single)
        except:
            subject_list=[]
        self.fields['subject_id'].choices=subject_list

    session_list=[]
    try:
        sessions = SessionYearModel.object.all()
        for session in sessions:
            session_single = (session.id,str(session.session_start_year)+" to "+str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list=[]

    subject_id=forms.ChoiceField(label="Subject",widget=forms.Select(attrs={"class":"form-control"}))
    session_ids=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"}))
    assignment_marks=forms.CharField(label="Assignment Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
    exam_marks=forms.CharField(label="Exam Marks",widget=forms.TextInput(attrs={"class":"form-control"}))