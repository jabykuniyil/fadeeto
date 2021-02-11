from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usersignin/', views.usersignin, name='usersignin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('userturfview/<int:id>/', views.turfview, name='userturfview'),
    path('category/<int:id>/', views.category, name="category"),
    path('userbooking/<int:id>/', views.userbooking, name='userbooking'),
    path('userlogout/', views.logout, name='logout'),
    path('bookhistory/', views.bookHistory, name='bookhistory')
]