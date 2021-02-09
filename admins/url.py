from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.adminsignin, name='adminsignin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('users/', views.users, name='users'),
    path('logout/', views.logout, name='logout'),
    path('vendors/', views.vendors, name='vendors'),
    path('facilities/', views.facilities, name='facilities'),
    path('category/', views.category, name='category'),
    path('addfacilities/', views.addFacilities, name='addfacilities'),
    path('addcategory/', views.addCategory, name='addcategory'),
    path('deletecategory/<int:id>/', views.deleteCategory, name='deletecategory'),
    path('editcategory/<int:id>/', views.editCategory, name='editcategory'),
    path('turfs/', views.turfs, name='turfs'),
    path('bookingsummary/', views.bookingSummary, name='bookingsummary')
]