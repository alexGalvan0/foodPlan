from calendar import FRIDAY, MONDAY, SATURDAY, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Custom_user(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email =  models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    #is_superuser = None
    #is_staff = None
    groups = None
    user_permissions = None
    last_login = None

    AUTH_USER_MODEL = 'account.user'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
            return self.name

class Meal(models.Model):
    
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'

    days_in_the_week = [(MONDAY,'Monday'),
                        (TUESDAY,'Tuesday'),
                        (WEDNESDAY,'Wednesday'),
                        (THURSDAY,'Thursday'),
                        (FRIDAY,'Friday'),
                        (SATURDAY,'Saturday'),
                        (SUNDAY,'Sunday')]

    name = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=100,null=True)
    day = models.CharField(max_length=100,choices=days_in_the_week,default=MONDAY)
    created = models.DateTimeField(auto_now=True,null=True)
    user = models.ForeignKey(Custom_user, default=None,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.name

 