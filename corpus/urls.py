from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recover_pass/', views.recover_pass_view, name='recover_pass'),
    path('recover_confirm/<str:uidb64>/<str:token>/', views.recover_confirm_view, name='recover_confirm'),
    path('recover_email/', views.recover_email_view, name='recover_email'),
    path('add_travel/', views.add_travel_view, name='add_travel'),
    path('add_plane/', views.add_plane_view, name='add_plane'),
    path('add_passenger/', views.add_passenger_view, name='add_passenger'),
    path('travel/<int:travel_id>/', views.travel_detail_view, name='travel_detail'),
    path('travel/state/', views.travel_state_view, name='travel_state'),
    path('passenger/modify/<int:passenger_id>', views.modify_passenger_view, name='modify_passenger'),
    path('passenger/eliminate/<int:passenger_id>', views.eliminate_passenger_view, name='eliminate_passenger'),
    path('profile/',views.profile_view, name='profile'),
    path('contact/',views.contact_view, name='contact'),
    path('support/',views.support_view, name='support'),
    path('aeronova/',views.aeronova_view, name='aeronova'),    
]
