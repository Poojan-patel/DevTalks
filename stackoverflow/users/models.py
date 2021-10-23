from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    # profile_pic, profession, organization, birthdate, age, mobile_no, country, skills
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.CharField(max_length=255, blank=True)
    profession = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True)
    age = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    country = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)
