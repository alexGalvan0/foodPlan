from django.urls import path
from rest_framework.authtoken import views


from .views import (MealView,
                    RegisterMealItem,
                    Custom_userView,
                    LoginView,
                    LogoutView,
                    RegisterView,
                    DeleteMealItem)

urlpatterns = [
    path('mealItems/',MealView.as_view()),
    path('add-meal/',RegisterMealItem.as_view()),
    path('delete-meal/',DeleteMealItem.as_view()),
    path('register',RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', Custom_userView.as_view()),
    path('logout', LogoutView.as_view()),
]
