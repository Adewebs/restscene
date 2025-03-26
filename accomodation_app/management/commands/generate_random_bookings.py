from decimal import Decimal
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from accomodation_app.models import Booking, ApartmentType
from auth_app.models import UserInfo
from django.utils.timezone import now
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate 20 random bookings for apartments'

    def handle(self, *args, **kwargs):
        # Get the user with id=1 (the host)
        host = UserInfo.objects.get(id=1)

        # Get all available apartment types
        apartment_types = ApartmentType.objects.all()

        # Generate 20 random bookings
        for _ in range(20):
            # Randomly select an apartment type
            apartment_type = random.choice(apartment_types)

            # Randomly select check-in and check-out dates within a reasonable range
            checkin_date = now() + timedelta(days=random.randint(1, 30))  # Check-in within the next 30 days
            checkout_date = checkin_date + timedelta(days=random.randint(1, 7))  # Checkout 1-7 days after check-in

            # Randomly select number of adults and children
            adults = random.randint(1, apartment_type.max_adults)
            children = random.randint(0, apartment_type.max_children)

            # Randomly select a total price (within the price range)
            price_range_start = float(apartment_type.price_range_start)
            price_range_end = float(apartment_type.price_range_end)
            total_price = Decimal(random.uniform(price_range_start, price_range_end))

            # Randomly choose a country (using COUNTRY_CHOICES)
            country = random.choice([code for code, _ in settings.COUNTRY_CHOICES])

            # Create the booking object
            booking = Booking.objects.create(
                guest=host,  # The host user with id=1
                apartment_type=apartment_type,
                checkin_date=checkin_date,
                checkin_out_date=checkout_date,
                total_price=total_price,
                is_paid=random.choice([True, False]),
                full_name=host.first_name + ' ' + host.last_name,
                email=host.email,
                phone=host.phone_number,
                mobile=host.phone_number,
                city=apartment_type.city,
                country=country,
                adults=adults,
                children=children,
                message="Random message for booking",
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created booking {booking.id}'))
