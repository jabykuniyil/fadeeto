from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    # path('users/', views.users, name='users'),
    path('turfs/', views.turfs, name='turfs'),
    path('editturf/<int:id>/', views.editTurf, name='edit'),
    # path('update/<int:id>', views.update, name='update'),
    path('deleteturf/<int:id>/', views.deleteTurf, name='delete'),
    path('bookhistory/', views.bookHistory, name='bookhistory'),
    path('addturf/', views.addTurf, name='addturf'),
    path('bookspecific/', views.book_specific, name="bookspecific"),
    path('vendorbooking/<int:id>/', views.vendor_booking, name='vendorbooking'),
    path('booksummary/<int:id>/', views.book_summary, name='booksummary'),
    path('bookrequests/', views.book_requests, name='bookrequests'),
    path('accept/<int:id>/', views.accept_booking, name='acceptbooking'),
    path('reject/<int:id>/', views.reject_booking, name='rejectbooking'),
    path('logout/', views.logout, name='logout')
]
