from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from courses.models import Subject, Course
from accounts.models import UserRole

User = get_user_model()


class CourseEnrollmentTest(APITestCase):
    """Test course enrollment"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create teacher
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        # Create student
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123'
        )
        self.student.role = UserRole.STUDENT
        self.student.is_active = True
        self.student.save()
        
        # Create subject and course
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
        
        self.enroll_url = reverse('student-course-enroll', kwargs={'pk': self.course.id})
    
    def test_enroll_in_course_success(self):
        """Test student can enroll in course"""
        self.client.force_authenticate(user=self.student)
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.course.students.filter(id=self.student.id).exists())
    
    def test_enroll_already_enrolled(self):
        """Test enrolling in already enrolled course"""
        self.client.force_authenticate(user=self.student)
        self.course.students.add(self.student)
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_enroll_own_course(self):
        """Test teacher cannot enroll in their own course"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_enroll_unauthenticated(self):
        """Test enrolling without authentication"""
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_enroll_nonexistent_course(self):
        """Test enrolling in non-existent course"""
        self.client.force_authenticate(user=self.student)
        url = reverse('student-course-enroll', kwargs={'pk': 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EnrolledCoursesTest(APITestCase):
    """Test listing enrolled courses"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create teacher
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        # Create student
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123'
        )
        self.student.role = UserRole.STUDENT
        self.student.is_active = True
        self.student.save()
        
        # Create subject and courses
        self.subject = Subject.objects.create(
            title='Programming',
            slug='programming'
        )
        
        self.course1 = Course.objects.create(
            owner=self.teacher,
            subject=self.subject,
            title='Python Course',
            overview='Learn Python'
        )
        
        self.course2 = Course.objects.create(
            owner=self.teacher,
            subject=self.subject,
            title='Django Course',
            overview='Learn Django'
        )
        
        # Enroll student in courses
        self.course1.students.add(self.student)
        self.course2.students.add(self.student)
        
        self.enrolled_url = reverse('student-courses-enrolled')
    
    def test_list_enrolled_courses(self):
        """Test student can list their enrolled courses"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.enrolled_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_list_enrolled_courses_unauthenticated(self):
        """Test listing enrolled courses without authentication"""
        response = self.client.get(self.enrolled_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_enrolled_courses_empty(self):
        """Test listing enrolled courses when not enrolled in any"""
        new_student = User.objects.create_user(
            email='newstudent@example.com',
            password='testpass123'
        )
        new_student.role = UserRole.STUDENT
        new_student.is_active = True
        new_student.save()
        
        self.client.force_authenticate(user=new_student)
        response = self.client.get(self.enrolled_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class StudentCourseAccessTest(APITestCase):
    """Test student access to course content"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create teacher
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='testpass123'
        )
        self.teacher.role = UserRole.TEACHER
        self.teacher.is_active = True
        self.teacher.save()
        
        # Create students
        self.enrolled_student = User.objects.create_user(
            email='enrolled@example.com',
            password='testpass123'
        )
        self.enrolled_student.role = UserRole.STUDENT
        self.enrolled_student.is_active = True
        self.enrolled_student.save()
        
        self.not_enrolled_student = User.objects.create_user(
            email='notenrolled@example.com',
            password='testpass123'
        )
        self.not_enrolled_student.role = UserRole.STUDENT
        self.not_enrolled_student.is_active = True
        self.not_enrolled_student.save()
        
        # Create course
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
        
        # Enroll one student
        self.course.students.add(self.enrolled_student)
    
    def test_enrolled_student_count(self):
        """Test course has correct number of enrolled students"""
        self.assertEqual(self.course.students.count(), 1)
    
    def test_student_is_enrolled(self):
        """Test checking if student is enrolled"""
        self.assertTrue(
            self.course.students.filter(id=self.enrolled_student.id).exists()
        )
        self.assertFalse(
            self.course.students.filter(id=self.not_enrolled_student.id).exists()
        )
