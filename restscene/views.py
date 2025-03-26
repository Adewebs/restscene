from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from accomodation_app.models import ApartmentType
# Create your views here.


def homepageapp(request):
    get_all_available_apartment = ApartmentType.objects.filter(availability_status=True)
    page = "RestScene" + ' | Home'

    context = {
                'pagetitle': page,
                "apartments":get_all_available_apartment
                   }
    return render(request, 'landing/index.html', context)
