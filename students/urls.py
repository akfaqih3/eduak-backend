from django.urls import path
from .views import (
    CourseEnrollAPI,
    CoursesEnrolledAPI,
)

urlpatterns = [
    path('courses/<int:pk>/enroll/', CourseEnrollAPI.as_view(), name='student-course-enroll'),
    path('courses/enrolled/', CoursesEnrolledAPI.as_view(), name='student-courses-enrolled'),
]