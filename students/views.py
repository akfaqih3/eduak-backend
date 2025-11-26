from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from courses.models import (
    Course,
)
from .serializers import (
    CourseJoinSerializer,
    ModuleSerializer,
)


from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Students'])
class CourseEnrollAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        user = request.user
        if course.owner == user:
            return Response(
                {'detail': 'You cannot enroll in your own course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user in course.students.all():
            return Response(
                {'detail': 'You are already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        course.students.add(user)
        return Response(
            {'detail': 'You have enrolled in this course'},
            status=status.HTTP_200_OK
        )
        
@extend_schema(tags=['Students'])
class CoursesEnrolledAPI(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CourseJoinSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.courses_joined.select_related('owner', 'subject').prefetch_related('students').all()