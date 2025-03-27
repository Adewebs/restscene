from django.urls import path,include
from . import views,dashboard

urlpatterns = [
    path('', views.homepageapp, name='home'),
    path('aboutus', views.about_us, name='aboutus'),
    path('contactus', views.contact_us, name='contactus'),
    path('book_reservation', views.book_reservation, name='book_reservation'),
    path('book_reservation_listing', views.book_reservation_listing, name='book_reservation_listing'),
    path('rooms/<int:pk>/', views.room_information, name='room'),
]