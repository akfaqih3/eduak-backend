from django.urls import path
from .views import (
    SubjectViewSet,
    CourseListAPI,
    CourseDetailAPI,
)

urlpatterns = [
    path('subjects/', SubjectViewSet.as_view({'get': 'list'}), name='subject-list'),
    path('subjects/<slug:slug>/', SubjectViewSet.as_view({'get': 'retrieve'}), name='subject-detail'),

    path('', CourseListAPI.as_view(), name='course-list'),
    path('<int:id>/', CourseDetailAPI.as_view(), name='course-detail'),
]