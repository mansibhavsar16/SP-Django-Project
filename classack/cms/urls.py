from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
   
    path('',views.home_view,name=''),

    path('teacherclick', views.teacherclick_view),
    path('studentclick', views.studentclick_view),

    path('studentsignup', views.student_signup_view,name='studentsignup'),
    
    path('studentlogin', LoginView.as_view(template_name='studentlogin.html')),
    path('teacherlogin', LoginView.as_view(template_name='teacherlogin.html')),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-view-student', views.teacher_view_student_view,name='teacher-view-student'),
    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance/<str:cl>', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:cl>', views.teacher_view_attendance_view,name='teacher-view-attendance'),
    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-attendance', views.student_attendance_view,name='student-attendance'),

    path('teacher-upload-document', views.DocumentCreateView.as_view(), name='teacher-upload-document'),
    path('student-view-document',views.DocumentListView.as_view(), name='student-view-document'),
    
    path('download/<int:document_id>/', views.download, name='download'),  
          
    path('student-marks',views.student_marks_view, name="student-marks")
]
