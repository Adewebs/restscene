from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from accomodation_app.models import ApartmentType,Booking
from django.conf import settings
from datetime import datetime
# Create your views here.


def homepageapp(request):
    get_all_available_apartment = ApartmentType.objects.filter(availability_status=True)
    page = "RestScene" + ' | Home'

    context = {
                'pagetitle': page,
                "apartment_types":get_all_available_apartment,
        'country_choices': settings.COUNTRY_CHOICES,
    }
    return render(request, 'landing/index.html', context)


def book_reservation(request):
    if request.method == 'POST':
        try:
            # Get data from the POST request
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            mobile = request.POST.get('mobile')
            city = request.POST.get('city')
            country = request.POST.get('country')
            adults = int(request.POST.get('adults'))
            children = int(request.POST.get('children'))
            checkin_date_str = request.POST.get('from')  # MM/DD/YYYY format
            checkout_date_str = request.POST.get('to')  # MM/DD/YYYY format
            apartment_type_id = request.POST.get('apartment_type')
            message = request.POST.get('message')

            # Find the apartment type based on the ID provided
            apartment_type = ApartmentType.objects.get(id=apartment_type_id)
            # Convert date strings to datetime objects (MM/DD/YYYY to YYYY-MM-DD)
            checkin_date = datetime.strptime(checkin_date_str, '%m/%d/%Y')
            checkout_date = datetime.strptime(checkout_date_str, '%m/%d/%Y')
            # Calculate total price (example)
            total_price = apartment_type.price_range_start  # This should be dynamic based on your pricing logic
            #TODO
            #process payment and set is_piad to true
            #also grab the apartment type and ensure is_avalable is false, because it has
            #been booked
            # Create a booking instance
            booking = Booking.objects.create(
                guest=request.user,
                apartment_type=apartment_type,
                full_name=request.user.first_name +" "+ request.user.last_name,
                email=email,
                phone=phone,
                mobile=mobile,
                city=city,
                country=country,
                adults=adults,
                children=children,
                checkin_date=checkin_date,
                checkin_out_date=checkout_date,
                total_price=total_price,
                message=message,
            )

            # Return a success response
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

