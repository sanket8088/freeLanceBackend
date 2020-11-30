
from django.db import models
from api.user.models import User

import datetime

# Create your models here.

class Response(models.Model):
    class Meta:
        verbose_name_plural = "Response"
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    response= models.CharField(max_length = 50, blank=True, null=True)
    respose_email = models.CharField(max_length = 50, blank=True, null=True)
    description = models.CharField(max_length = 1000, blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.orderNo