from django.urls import path, include
from .views import (
    CourseCreateAPI,
    CourseListAPI,
    CourseDetailAPI,
    CourseUpdateAPI,    
    CourseDeleteAPI,
)

urlpatterns = [
    path('courses/', CourseListAPI.as_view(), name='teacher-course-list'),
    path('courses/create/', CourseCreateAPI.as_view(), name='teacher-course-create'),
    path('courses/<int:pk>/', CourseDetailAPI.as_view(), name='teacher-course-detail'),
    path('courses/<int:pk>/update/', CourseUpdateAPI.as_view(), name='teacher-course-update'),
    path('courses/<int:pk>/delete/', CourseDeleteAPI.as_view(), name='teacher-course-delete'),
]