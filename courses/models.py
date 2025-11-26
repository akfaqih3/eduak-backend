from typing import Iterable
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


User = get_user_model()

class Subject(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    photo = models.ImageField(
        upload_to='courses/subjects/photos/%Y/%m/%d/',
        blank=True
        )
    
    @property
    def total_courses(self) -> int:
        return self.courses.count()

    class Meta:
        ordering = ['title']
        

    def __str__(self):
        return self.title
    
class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE,
        db_index=True
    )

    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        db_index=True
    )

    title = models.CharField(max_length=200, db_index=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    students = models.ManyToManyField(
        User,
        related_name='courses_joined',
        blank=True
    )
    photo = models.ImageField(
        upload_to='courses/courses/photos/%Y/%m/%d/',
        blank=True
        )
    
    @property
    def total_students(self) -> int:
        return self.students.count()
    
    @property
    def total_modules(self) -> int:
        return self.modules.count()
    


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['subject', '-created']),
            models.Index(fields=['owner', '-created']),
            models.Index(fields=['title', '-created']),
        ]

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    photo = models.ImageField(
        upload_to='courses/courses/modules/photos/%Y/%m/%d/',
        blank=True
        )

    class Meta:
        ordering = ['order']
    def __str__(self):
        return f'{self.order}. {self.title}'
    

class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':('text', 'video', 'image', 'file')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )

    def __str__(self):
        return self.title
    

    

class Text(ItemBase):
    content = models.TextField()
    
    def is_text(self):
        return True

class File(ItemBase):
    file = models.FileField(upload_to='files')
    
    def is_file(self):
        return True


class Image(ItemBase):
    file = models.FileField(upload_to='images')

    def is_image(self):
        return True
    
class Video(ItemBase):
    url = models.URLField()

    def is_video(self):
        return True



