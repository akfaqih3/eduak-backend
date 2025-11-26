from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from courses.models import Subject, Course, Module

User = get_user_model()


class SubjectModelTest(TestCase):
    """Test Subject model"""
    
    def setUp(self):
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
    
    def test_subject_creation(self):
        """Test subject is created correctly"""
        self.assertEqual(self.subject.title, 'Programming')
        self.assertEqual(self.subject.slug, 'programming')
        self.assertEqual(str(self.subject), 'Programming')
    
    def test_subject_total_courses(self):
        """Test total_courses property"""
        user = User.objects.create_user(email='test@example.com', password='pass123')
        Course.objects.create(
            owner=user,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        self.assertEqual(self.subject.total_courses, 1)


class CourseModelTest(TestCase):
    """Test Course model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python from scratch'
        )
    
    def test_course_creation(self):
        """Test course is created correctly"""
        self.assertEqual(self.course.title, 'Python Course')
        self.assertEqual(self.course.owner, self.user)
        self.assertEqual(self.course.subject, self.subject)
        self.assertEqual(str(self.course), 'Python Course')
    
    def test_course_total_students(self):
        """Test total_students property"""
        student = User.objects.create_user(email='student@example.com', password='pass123')
        self.course.students.add(student)
        self.assertEqual(self.course.total_students, 1)
    
    def test_course_total_modules(self):
        """Test total_modules property"""
        Module.objects.create(
            course=self.course,
            title='Introduction',
            description='Intro module'
        )
        self.assertEqual(self.course.total_modules, 1)


class SubjectAPITest(APITestCase):
    """Test Subject API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        self.list_url = reverse('subject-list')
    
    def test_list_subjects(self):
        """Test listing subjects"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_subject(self):
        """Test retrieving a subject"""
        url = reverse('subject-detail', kwargs={'slug': self.subject.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], self.subject.title)


class CourseAPITest(APITestCase):
    """Test Course API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        self.list_url = reverse('course-list')
    
    def test_list_courses(self):
        """Test listing courses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_retrieve_course(self):
        """Test retrieving a course"""
        url = reverse('course-detail', kwargs={'id': self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)
    
    def test_filter_courses_by_subject(self):
        """Test filtering courses by subject"""
        response = self.client.get(self.list_url, {'subject__slug': 'programming'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_courses(self):
        """Test searching courses"""
        response = self.client.get(self.list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
