from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homepageapp, name='home'),
    path('book_reservation', views.book_reservation, name='book_reservation'),
    path('book_reservation_listing', views.book_reservation_listing, name='book_reservation_listing'),
    path('rooms/<int:pk>/', views.room_information, name='room'),
]