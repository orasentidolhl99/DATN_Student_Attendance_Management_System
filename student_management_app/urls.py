from django.urls import path, include
from . import views
from .controllers import admin_views, teacher_views, student_views
from django.conf.urls.static import static
from student_management_system import settings


urlpatterns = [
    path('', views.loginPage, name="login"),    
    
    path('doLogin', views.doLogin, name="doLogin"),
    path('profile_teams', views.profile_teams, name = "profile_teams"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', admin_views.admin_home, name="admin_home"),
    
    path('add_teacher/', admin_views.add_teacher, name="add_teacher"),
    path('add_teacher_save/', admin_views.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', admin_views.manage_teacher, name="manage_teacher"),
    path('edit_teacher/<teacher_id>/', admin_views.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save/', admin_views.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<teacher_id>/', admin_views.delete_teacher, name="delete_teacher"),
    
    path('add_course/', admin_views.add_course, name="add_course"),
    path('add_course_save/', admin_views.add_course_save, name="add_course_save"),
    path('manage_course/', admin_views.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', admin_views.edit_course, name="edit_course"),
    path('edit_course_save/', admin_views.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/', admin_views.delete_course, name="delete_course"),
    
    path('manage_session/', admin_views.manage_session, name="manage_session"),
    path('add_session/', admin_views.add_session, name="add_session"),
    path('add_session_save/', admin_views.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', admin_views.edit_session, name="edit_session"),
    path('edit_session_save/', admin_views.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', admin_views.delete_session, name="delete_session"),
    
    path('add_student/', admin_views.add_student, name="add_student"),
    path('add_student_save/', admin_views.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', admin_views.edit_student, name="edit_student"),
    path('edit_student_save/', admin_views.edit_student_save, name="edit_student_save"),
    path('manage_student/', admin_views.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', admin_views.delete_student, name="delete_student"),
    
    path('add_image_detect/<username>/<last_name>/<first_name>', admin_views.add_image_detect, name="add_image_detect"),
    path('add_image_detect_save/', admin_views.add_image_detect_save, name="add_image_detect_save"),
    
    path('add_subject/', admin_views.add_subject, name="add_subject"),
    path('add_subject_save/', admin_views.add_subject_save, name="add_subject_save"),
    path('manage_subject/', admin_views.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', admin_views.edit_subject, name="edit_subject"),
    path('edit_subject_save/', admin_views.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', admin_views.delete_subject, name="delete_subject"),
    
    path('check_email_exist/', admin_views.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', admin_views.check_username_exist, name="check_username_exist"),
    
    path('student_feedback_message/', admin_views.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', admin_views.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('teacher_feedback_message/', admin_views.teacher_feedback_message, name="teacher_feedback_message"),
    path('teacher_feedback_message_reply/', admin_views.teacher_feedback_message_reply, name="teacher_feedback_message_reply"),
    
    # path('student_leave_view/', admin_views.student_leave_view, name="student_leave_view"),
    # path('student_leave_approve/<leave_id>/', admin_views.student_leave_approve, name="student_leave_approve"),
    # path('student_leave_reject/<leave_id>/', admin_views.student_leave_reject, name="student_leave_reject"),
    path('teacher_leave_view/', admin_views.teacher_leave_view, name="teacher_leave_view"),
    path('teacher_leave_approve/<leave_id>/', admin_views.teacher_leave_approve, name="teacher_leave_approve"),
    path('teacher_leave_reject/<leave_id>/', admin_views.teacher_leave_reject, name="teacher_leave_reject"),
    
    path('admin_view_attendance/', admin_views.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', admin_views.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', admin_views.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', admin_views.admin_profile, name="admin_profile"),
    path('admin_profile_update/', admin_views.admin_profile_update, name="admin_profile_update"),
    
    path('add_student_subject_link/<subject_id>/', admin_views.add_student_subject_link, name="add_student_subject_link"),
    path('add_student_subject_link_save/<subject_id>/', admin_views.add_student_subject_link_save, name="add_student_subject_link_save"),
    path('manage_student_subject_link/<subject_id>/', admin_views.manage_student_subject_link, name="manage_student_subject_link"),
    path('delete_student_subject_link/<student_subject_id>/', admin_views.delete_student_subject_link, name="delete_student_subject_link"),
    

     # URLS for teacher
    path('teacher_home/', teacher_views.teacher_home, name="teacher_home"),
    path('teacher_take_attendance', teacher_views.teacher_take_attendance, name="teacher_take_attendance"),
    path('get_students/', teacher_views.get_students, name="get_students"),
    path('save_attendance_data/', teacher_views.save_attendance_data, name="save_attendance_data"),
    path('teacher_update_attendance/', teacher_views.teacher_update_attendance, name="teacher_update_attendance"),
    path('get_attendance_dates/', teacher_views.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', teacher_views.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', teacher_views.update_attendance_data, name="update_attendance_data"),
    path('teacher_apply_leave/', teacher_views.teacher_apply_leave, name="teacher_apply_leave"),
    path('teacher_apply_leave_save/', teacher_views.teacher_apply_leave_save, name="teacher_apply_leave_save"),
    path('teacher_feedback/', teacher_views.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save/', teacher_views.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_profile/', teacher_views.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', teacher_views.teacher_profile_update, name="teacher_profile_update"),
    path('teacher_add_result/', teacher_views.teacher_add_result, name="teacher_add_result"),
    path('teacher_add_result_save/', teacher_views.teacher_add_result_save, name="teacher_add_result_save"),
    path('student_leave_view/', teacher_views.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', teacher_views.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', teacher_views.student_leave_reject, name="student_leave_reject"),
    path('teacher_manage_subject/', teacher_views.teacher_manage_subject, name="teacher_manage_subject"),
    path('teacher_manage_student_subject_link/<subject_id>/', teacher_views.teacher_manage_student_subject_link, name="teacher_manage_student_subject_link"),
    path('teacher_create_attendance/', teacher_views.teacher_create_attendance, name="teacher_create_attendance"),
    path('teacher_view_attendance/', teacher_views.teacher_view_attendance, name="teacher_view_attendance"),
    path('turn_off_attendance/', teacher_views.turn_off_attendance, name="turn_off_attendance"),
    
    
    # URLS for Teacher - Detect student
    path('take_attendance_detect/', teacher_views.take_attendance_detect, name='take_attendance_detect'),
    path('facecam_feed', teacher_views.facecam_feed, name='facecam_feed'),
    path('attendance_result_stream/', teacher_views.attendance_result_stream, name='attendance_result_stream'),
    path('save_detect_attendance_data/', teacher_views.save_detect_attendance_data, name='save_detect_attendance_data'),
    path('test_stop_camera/', teacher_views.test_stop_camera, name='test_stop_camera'),
    
    # URLS for Student
    path('student_home/', student_views.student_home, name="student_home"),
    path('student_view_attendance/', student_views.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', student_views.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', student_views.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', student_views.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', student_views.student_feedback, name="student_feedback"),
    path('student_feedback_save/', student_views.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', student_views.student_profile, name="student_profile"),
    path('student_profile_update/', student_views.student_profile_update, name="student_profile_update"),
    path('student_view_result/', student_views.student_view_result, name="student_view_result"),
    path('student_create_attendance/', student_views.student_create_attendance, name="student_create_attendance"),
    path('student_create_attendance_detect/', student_views.student_create_attendance_detect, name="student_create_attendance_detect"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)