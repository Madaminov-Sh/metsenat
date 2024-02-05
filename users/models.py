from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken

from common.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return self.username
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
    
    class Meta:
        verbose_name_plural = 'Users'
        

class Sponsor(BaseModel):
    donated = models.IntegerField()
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    
    student = models.ManyToManyRel('Student', models.CASCADE, related_name='students')
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = 'Sponsors'
        

class Student(BaseModel):
    class StudyType(models.TextChoices):
        bachelor = 'bachelor', 'Bachelor'
        master = 'master', 'Master'
        doctoral = 'doctoral', 'Doctoral'
        
    image = models.ImageField(upload_to='students/')
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14, unique=True)    
    university = models.CharField(max_length=255)
    study_type = models.CharField(max_length=10, choices=StudyType.choices, default=StudyType.bachelor)
    
    contract = models.IntegerField()
    donated = models.IntegerField()
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = 'Students'
