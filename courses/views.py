from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import (
    Subject,
    Course,
)
from .serializers import (
    SubjectsOutputSerializer,
    SubjectCoursesOutputSerializer,
    CourseSerializer,
)

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Courses'])
class SubjectViewSet(viewsets.ViewSet):
    
    queryset = Subject.objects.prefetch_related('courses').all()
    serializer_class = SubjectsOutputSerializer
    retrieve_serializer_class = SubjectCoursesOutputSerializer
    permission_classes = []
    authentication_classes = []
    pagination_class = LimitOffsetPagination

    def list(self, request):
        queryset = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, slug):
        subject = self.queryset.get(slug=slug)
        queryset = subject.courses.select_related('owner', 'subject').prefetch_related('students').all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.retrieve_serializer_class(page, many=True)
            return paginator.get_paginated_response({
                'subject': subject.title,
                'courses': serializer.data
            })
        serializer = self.retrieve_serializer_class(queryset, many=True)
        return Response(
            {
                'subject': subject.title,
                'courses': serializer.data
            }
        )
    
@extend_schema(tags=['Courses'])
class CourseListAPI(ListAPIView):
    queryset = Course.objects.select_related('owner', 'subject').prefetch_related('students').all()
    serializer_class = CourseSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = []
    authentication_classes = []
    pagination_class.default_limit = 10
    pagination_class.max_limit = 50
    pagination_class.limit_query_param = 'size'
    pagination_class.offset_query_param = 'index'

    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ['title','overview']
    filterset_fields = ['subject__slug','owner__name']
    ordering_fields = "__all__"
    ordering = ['-created']


@extend_schema(tags=['Courses'])
class CourseDetailAPI(RetrieveAPIView):
  queryset = Course.objects.select_related('owner', 'subject').prefetch_related('students', 'modules').all()
  serializer_class = CourseSerializer
  permission_classes = []
  authentication_classes = []

  pk_url_kwarg = 'id'
  lookup_field = 'id'
  
    