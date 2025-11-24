from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserRole(models.TextChoices):
    TEACHER = 'teacher'
    STUDENT = 'student'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.TEACHER, db_index=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email', 'role']),
            models.Index(fields=['is_active', 'role']),
        ]

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.user.email