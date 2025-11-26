from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from courses.models import Subject, Course
from accounts.models import UserRole

User = get_user_model()


class TeacherPermissionTest(TestCase):
    """Test teacher permissions"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123'
        )
        self.student.role = UserRole.STUDENT
        self.student.is_active = True
        self.student.save()
    
    def test_teacher_role(self):
        """Test teacher has correct role"""
        self.assertEqual(self.teacher.role, UserRole.TEACHER)
    
    def test_student_role(self):
        """Test student has correct role"""
        self.assertEqual(self.student.role, UserRole.STUDENT)


class CourseCreateTest(APITestCase):
    """Test course creation by teachers"""
    
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        
        self.create_url = reverse('teacher-course-create')
        self.client.force_authenticate(user=self.teacher)
    
    def test_create_course_success(self):
        """Test teacher can create course"""
        data = {
            'subject': self.subject.id,
            'title': 'Python Course',
            'overview': 'Learn Python from scratch'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.filter(title='Python Course').exists())
    
    def test_create_course_unauthenticated(self):
        """Test creating course without authentication"""
        self.client.force_authenticate(user=None)
        data = {
            'subject': self.subject.id,
            'title': 'Python Course',
            'overview': 'Learn Python'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeacherCourseListTest(APITestCase):
    """Test listing teacher's courses"""
    
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        
        self.course = Course.objects.create(
            owner=self.teacher,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        
        self.list_url = reverse('teacher-course-list')
        self.client.force_authenticate(user=self.teacher)
    
    def test_list_teacher_courses(self):
        """Test teacher can list their courses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CourseUpdateTest(APITestCase):
    """Test course update by owner"""
    
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        self.other_teacher = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        self.other_teacher.role = UserRole.TEACHER
        self.other_teacher.is_active = True
        self.other_teacher.save()
        
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        
        self.course = Course.objects.create(
            owner=self.teacher,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        
        self.update_url = reverse('teacher-course-update', kwargs={'pk': self.course.id})
    
    def test_update_own_course(self):
        """Test teacher can update their own course"""
        self.client.force_authenticate(user=self.teacher)
        data = {
            'subject': self.subject.id,
            'title': 'Advanced Python',
            'overview': 'Advanced Python concepts'
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Advanced Python')
    
    def test_update_other_course(self):
        """Test teacher cannot update other's course"""
        self.client.force_authenticate(user=self.other_teacher)
        data = {
            'subject': self.subject.id,
            'title': 'Hacked Course',
            'overview': 'Hacked'
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseDeleteTest(APITestCase):
    """Test course deletion by owner"""
    
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        
        self.course = Course.objects.create(
            owner=self.teacher,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        
        self.delete_url = reverse('teacher-course-delete', kwargs={'pk': self.course.id})
        self.client.force_authenticate(user=self.teacher)
    
    def test_delete_own_course(self):
        """Test teacher can delete their own course"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())
