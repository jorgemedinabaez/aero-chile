from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('travel/new/', views.add_travel, name='add_travel'),
    path('travel/new/register/', views.add_travel_register, name='add_travel_register'),
    path('travel/<str:code>/newpassenger/', views.add_passenger, name='add_passenger'),
    path('travel/<str:code>/newpassenger/register', views.add_passenger, name='add_passenger_register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('task/', views.task, name='task'),
]
