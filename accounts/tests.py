from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import Profile, UserRole

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_active)
        self.assertEqual(user.role, UserRole.TEACHER)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_user_str(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])


class ProfileModelTest(TestCase):
    """Test Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Test profile is created with user"""
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), self.user.email)


class UserRegistrationTest(APITestCase):
    """Test user registration"""
    
    def setUp(self):
        self.client = APIClient()
        # Create required groups
        Group.objects.get_or_create(name='teacher')
        Group.objects.get_or_create(name='student')
        
        self.register_url = reverse('user-register')
        self.valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '771234567',
            'role': 'teacher',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }
    
    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Error: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())
    
    def test_register_user_password_mismatch(self):
        """Test registration with password mismatch"""
        data = self.valid_data.copy()
        data['confirm_password'] = 'different'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email"""
        User.objects.create_user(email=self.valid_data['email'], password='pass123')
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OTPTest(APITestCase):
    """Test OTP functionality"""
    
    def setUp(self):
        self.client = APIClient()
        # Create required groups
        Group.objects.get_or_create(name='teacher')
        Group.objects.get_or_create(name='student')
        
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.send_otp_url = reverse('otp-send')
        self.verify_otp_url = reverse('otp-verify')
    
    def test_send_otp_success(self):
        """Test sending OTP"""
        response = self.client.post(self.send_otp_url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_send_otp_invalid_email(self):
        """Test sending OTP to non-existent email"""
        response = self.client.post(self.send_otp_url, {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserProfileTest(APITestCase):
    """Test user profile endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        # Create required groups
        Group.objects.get_or_create(name='teacher')
        Group.objects.get_or_create(name='student')
        
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.user.is_active = True
        self.user.save()
        Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('user-profile')
    
    def test_get_profile(self):
        """Test getting user profile"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_get_profile_unauthenticated(self):
        """Test getting profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
