from django.urls import path, include
from django.contrib import admin
import account 
from . import views
urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),

]
