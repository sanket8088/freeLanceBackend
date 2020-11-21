from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]
    session_token = models.CharField(max_length=100, default=0)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    organisation = models.CharField(max_length=100, blank=True)
    totalCredits = models.IntegerField(default=10)
    is_activated = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    reset_key = models.CharField(max_length=500, default=0)
    email_verified = models.CharField(max_length =5, default=0)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


#Search records table to made later



    
