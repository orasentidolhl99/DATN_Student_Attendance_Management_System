from django.urls import path, include
from . import views
from .import HodViews, TeacherViews, StudentViews


urlpatterns = [
    path('', views.loginPage, name="login"),    
    
    path('doLogin', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_teacher/', HodViews.add_teacher, name="add_teacher"),
    path('add_teacher_save/', HodViews.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', HodViews.manage_teacher, name="manage_teacher"),
    path('edit_teacher/<teacher_id>/', HodViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save/', HodViews.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<teacher_id>/', HodViews.delete_teacher, name="delete_teacher"),
    path('add_course/', HodViews.add_course, name="add_course"),
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
    path('manage_course/', HodViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"),
    path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"),
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session/', HodViews.add_session, name="add_session"),
    path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
    path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', HodViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', HodViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('teacher_feedback_message/', HodViews.teacher_feedback_message, name="teacher_feedback_message"),
    path('teacher_feedback_message_reply/', HodViews.teacher_feedback_message_reply, name="teacher_feedback_message_reply"),
    path('student_leave_view/', HodViews.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', HodViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', HodViews.student_leave_reject, name="student_leave_reject"),
    path('teacher_leave_view/', HodViews.teacher_leave_view, name="teacher_leave_view"),
    path('teacher_leave_approve/<leave_id>/', HodViews.teacher_leave_approve, name="teacher_leave_approve"),
    path('teacher_leave_reject/<leave_id>/', HodViews.teacher_leave_reject, name="teacher_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', HodViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    

     # URLS for teacher
    path('teacher_home/', TeacherViews.teacher_home, name="teacher_home"),
    path('teacher_take_attendance/', TeacherViews.teacher_take_attendance, name="teacher_take_attendance"),
    path('get_students/', TeacherViews.get_students, name="get_students"),
    path('save_attendance_data/', TeacherViews.save_attendance_data, name="save_attendance_data"),
    path('teacher_update_attendance/', TeacherViews.teacher_update_attendance, name="teacher_update_attendance"),
    path('get_attendance_dates/', TeacherViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', TeacherViews.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', TeacherViews.update_attendance_data, name="update_attendance_data"),
    path('teacher_apply_leave/', TeacherViews.teacher_apply_leave, name="teacher_apply_leave"),
    path('teacher_apply_leave_save/', TeacherViews.teacher_apply_leave_save, name="teacher_apply_leave_save"),
    path('teacher_feedback/', TeacherViews.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save/', TeacherViews.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_profile/', TeacherViews.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', TeacherViews.teacher_profile_update, name="teacher_profile_update"),
    path('teacher_add_result/', TeacherViews.teacher_add_result, name="teacher_add_result"),
    path('teacher_add_result_save/', TeacherViews.teacher_add_result_save, name="teacher_add_result_save"),

    # URLS for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
]