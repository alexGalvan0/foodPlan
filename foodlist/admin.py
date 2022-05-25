
from django.contrib import admin
from .models import Custom_user, Meal

# Register your models here.
admin.site.register(Meal)
admin.site.register(Custom_user)