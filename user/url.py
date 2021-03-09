from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map/<int:id>/', views.map, name='map'),
    path('usersignin/', views.usersignin, name='usersignin'),
    path('phone/', views.phone, name='phone'),
    path('otp/', views.otp, name='otp'),
    path('usersignup/', views.usersignup, name='usersignup'),
    # path('otpsignin/', views.otp_signin, name='otpsignin'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('userhistory/', views.user_history, name='userhistory'),
    path('userturfview/<int:id>/', views.turfview, name='userturfview'),
    path('category/<int:id>/', views.category, name="category"),
    path('userbooking/<int:id>/', views.userbooking, name='userbooking'),
    path('summary/', views.summary, name='summary'),
    path('coupon-selected/<int:id>/', views.coupon_selected, name='coupon-selected'),
    path('time-slots/<int:id>/', views.time_slots, name='time-slots'),
    path('userlogout/', views.logout, name='logout'),
    path('customer-review/<int:id>/', views.customer_review, name='customer-review')
]