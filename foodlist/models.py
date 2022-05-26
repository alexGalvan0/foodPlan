from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Custom_user(AbstractUser):
    name = models.CharField(max_length=255)
    email =  models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    AUTH_USER_MODEL = 'account.user'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
            return self.name

class Meal(models.Model):
    name = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=100,null=True)
    day = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(auto_now=True,null=True)
    user = models.ForeignKey(Custom_user, default=None,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.name

 