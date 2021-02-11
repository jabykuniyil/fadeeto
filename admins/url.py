from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.adminsignin, name='adminsignin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('users/', views.users, name='users'),
    path('blockusers/<int:id>/', views.block_user, name="blockusers"),
    path('logout/', views.logout, name='logout'),
    path('vendors/', views.vendors, name='vendors'),
    path('blockvendors/<int:id>/', views.block_vendor, name='blockvendors'),
    path('facilities/', views.facilities, name='facilities'),
    path('category/', views.category, name='category'),
    path('addfacilities/', views.addFacilities, name='addfacilities'),
    path('addcategory/', views.addCategory, name='addcategory'),
    path('editfacilities/<int:id>/', views.editFacilities, name="editfacilities"),
    path('deletefacility/<int:id>/', views.deleteFacility, name="deletefacility"),
    path('deletecategory/<int:id>/', views.deleteCategory, name='deletecategory'),
    path('editcategory/<int:id>/', views.editCategory, name='editcategory'),
    path('turfs/', views.turfs, name='turfs'),
    path('blockturf/<int:id>/', views.block_turf, name='blockturf'),
    path('bookingsummary/', views.bookingSummary, name='bookingsummary')
]