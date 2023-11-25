from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('travel/new/', views.add_travel, name='add_travel'),
    path('travel/new/register/', views.add_register_travel, name='add_register_travel'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('task/', views.task, name='task'),
]
