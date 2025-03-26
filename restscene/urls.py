from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homepageapp, name='home'),
    path('book_reservation', views.book_reservation, name='book_reservation'),
]