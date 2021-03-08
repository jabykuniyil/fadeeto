from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('turfs/', views.turfs, name='turfs'),
    path('editturf/<int:id>/', views.editTurf, name='edit'),
    path('deleteturf/<int:id>/', views.deleteTurf, name='delete'),
    path('bookhistory/', views.bookHistory, name='bookhistory'),
    path('addturf/', views.addTurf, name='addturf'),
    path('bookspecific/', views.book_specific, name="bookspecific"),
    path('vendorbooking/<int:id>/', views.vendor_booking, name='vendorbooking'),
    path('booksummary/<int:id>/', views.book_summary, name='booksummary'),
    path('bookrequests/', views.book_requests, name='bookrequests'),
    path('accept/<int:id>/', views.accept_booking, name='acceptbooking'),
    path('reject/<int:id>/', views.reject_booking, name='rejectbooking'),
    path('reviews/', views.reviews, name='reviews'),
    path('coupons/', views.coupons, name='coupons'),
    path('addcoupons/', views.add_coupons, name='addcoupons'),
    path('offers/', views.offers, name='offers'),
    path('addoffers/', views.add_offers, name='addoffers'),
    path('reports/', views.reports, name='reports'),
    path('logout/', views.logout, name='logout'),
]
