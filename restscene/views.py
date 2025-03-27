from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from accomodation_app.models import ApartmentType,Booking,ApartmentMedia
from django.conf import settings
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.


def homepageapp(request):
    if request.method == "POST":
        user_country = request.POST.get('country')
        request.session['user_country'] = user_country

        # Filter apartments based on the selected country
        get_all_available_apartment = ApartmentType.objects.filter(availability_status=True, country=user_country)
    else:
        # Default to 'US' if no country is selected
        user_country = request.session.get('user_country', 'US')
        get_all_available_apartment = ApartmentType.objects.filter(availability_status=True, country=user_country)

    # Get the number of apartments per page from the request or default to 3
    items_per_page = request.GET.get('items_per_page', 6)  # Default to 3 per page

    # Set up pagination
    paginator = Paginator(get_all_available_apartment, items_per_page)  # Paginate apartments
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page

    context = {
        'pagetitle': "RestScene | Home",
        'apartment_types': get_all_available_apartment,
        'apartment_listing_types': page_obj,
        'country_choices': settings.COUNTRY_CHOICES,
        'user_country': user_country,
        'items_per_page': items_per_page,  # Pass the current items per page value to the template
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
            country =  request.session.get('user_country', 'US')
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


def room_information(request,pk):
    get_room_information = ApartmentType.objects.get(pk=pk)
    media_element = ApartmentMedia.objects.filter(apartment=get_room_information)
    context = {
        'pagetitle': f"RestScene | {get_room_information.name}",
        'apartment_information': get_room_information,
        'media_element' : media_element

    }

    return render(request, 'landing/room_info.html', context)


def book_reservation_listing(request):
    if request.method == 'POST':
        try:
            # Get data from the POST request

            country =  request.session.get('user_country', 'US')
            adults = int(request.POST.get('adults'))
            children = int(request.POST.get('children'))
            checkin_date_str = request.POST.get('from')  # MM/DD/YYYY format
            checkout_date_str = request.POST.get('to')  # MM/DD/YYYY format
            apartment_type_id = request.POST.get('apartment_type')

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
                email=request.user.email,
                phone=request.user.phone_number,
                country=country,
                adults=adults,
                children=children,
                checkin_date=checkin_date,
                checkin_out_date=checkout_date,
                total_price=total_price,

            )

            # Return a success response
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})