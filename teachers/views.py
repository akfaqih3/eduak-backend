from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CourseInputSerializer,
    CourseOutputSerializer,
)
from .permissions import (
    IsTeacher,
    IsOwner,
)
from .services import (
    course_create,
    course_update,
    course_delete,
)
from .selectors import (
    course_list,
    course_detail,
)

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Teachers'], responses={201: CourseOutputSerializer})
class CourseCreateAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = CourseInputSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = course_create(
                owner=request.user,
                subject=serializer.data['subject'],
                title=serializer.data['title'],
                overview=serializer.data['overview'],
                photo=serializer.validated_data['photo'] if 'photo' in serializer.data else None
            )
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Teachers'])
class CourseListAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = CourseOutputSerializer
        
    def get_queryset(self):
        return course_list(owner=self.request.user)


    @extend_schema(operation_id="list_teacher_courses",)
    def get(self, request):
        courses = self.get_queryset()
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Teachers'])
class CourseDetailAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    serializer_class = CourseOutputSerializer
    def get_object(self, pk):
        coures = course_detail(pk=pk)
        self.check_object_permissions(self.request, coures)
        return coures

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = self.serializer_class(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=['Teachers'])
class CourseUpdateAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    serializer_class = CourseInputSerializer
    
    def get_object(self, pk):
        course = course_detail(pk=pk)
        self.check_object_permissions(self.request, course)
        return course
    
    def put(self, request, pk):
        # Check permissions first
        course = self.get_object(pk)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = course_update(
                pk=pk,
                subject=serializer.data['subject'],
                title=serializer.data['title'],
                overview=serializer.data['overview'],
                photo=serializer.validated_data['photo'] if 'photo' in serializer.data else None
            )
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(tags=['Teachers'])
class CourseDeleteAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    serializer_class = None
    def get_object(self, pk):
        course = course_detail(pk=pk)
        self.check_object_permissions(self.request, course)
        return course
    
    def delete(self, request, pk):
        course_delete(self.get_object(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)