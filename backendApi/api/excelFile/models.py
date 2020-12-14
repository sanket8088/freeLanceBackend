
from django.db import models
from api.user.models import User

import datetime

# Create your models here.

class SendMailSave(models.Model):
    class Meta:
        verbose_name_plural = "MailSend"
    
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length = 500, blank=True, null=True)
    instructions = models.CharField(max_length = 500, blank=True, null=True)
    attention = models.CharField(max_length = 500, blank=True, null=True)
    message = models.CharField(max_length = 500, blank=True, null=True)
    footer = models.CharField(max_length = 500, blank=True, null=True)
    toMail = models.CharField(max_length=500, blank=True, null=True)
    organization = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    # cc= models.CharField(max_length=2000, blank=True, null=True)
    amount = models.CharField(max_length=500, blank=True, null=True)
    responded = models.IntegerField(default=0, null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Response(models.Model):
    class Meta:
        verbose_name_plural = "Response"
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    emailReply = models.ForeignKey(SendMailSave, on_delete=models.CASCADE, null=True)
    response= models.CharField(max_length = 50, blank=True, null=True)
    respose_email = models.CharField(max_length = 50, blank=True, null=True)
    description = models.CharField(max_length = 1000, blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.orderNo