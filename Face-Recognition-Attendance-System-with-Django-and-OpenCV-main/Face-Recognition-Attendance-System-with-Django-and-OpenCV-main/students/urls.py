from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Face capture
    path('students/<str:student_id>/capture-face/', views.capture_face, name='capture_face'),
    path('students/<str:student_id>/save-face/', views.save_face_encoding, name='save_face_encoding'),
    
    # Face search
    path('search-face/', views.search_face, name='search_face'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/realtime/', views.realtime_attendance, name='realtime_attendance'),
    path('video-feed/', views.video_feed, name='video_feed'),
    
    # Departments (ADDED MISSING URLS)
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/update/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
]
