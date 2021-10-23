from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    profile_picture = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    bio = models.CharField(max_length=255, blank=True)
    profession = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    country = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)
