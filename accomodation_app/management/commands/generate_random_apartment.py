import random
from django.core.management.base import BaseCommand
from auth_app.models import UserInfo
from accomodation_app.models import ApartmentType
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create 20 random apartment types and assign them to the user with id=1'

    def handle(self, *args, **kwargs):
        try:
            # Get the user with id=1 (Make sure the user exists)
            user = UserInfo.objects.get(id=1)

            # List of possible apartment names and countries
            apartment_names = [
                'Featured', 'Master Suite', 'Mini Suite', 'Ultra Deluxe', 'Luxury Room',
                'Premium Room', 'Normal Room'
            ]
            countries = ['NG', 'GH', 'KE', 'ZA', 'UG', 'US', 'GB', 'CA', 'AE']
            cities = ['Lagos', 'Accra', 'Nairobi', 'Cape Town', 'Kampala', 'New York', 'London', 'Toronto', 'Dubai']

            # Create 20 random apartment types
            for _ in range(20):
                name = random.choice(apartment_names)
                price_range_start = random.uniform(100.0, 500.0)
                price_range_end = price_range_start + random.uniform(50.0, 200.0)
                city = random.choice(cities)
                country = random.choice(countries)

                # Create a random ApartmentType object
                ApartmentType.objects.create(
                    name=name,
                    host=user,  # Assign user with id=1 as the host
                    description=f"This is a {name} apartment in {city}, {country}",
                    rating=random.uniform(1.0, 5.0),  # Random rating between 1 and 5
                    max_adults=random.randint(1, 5),  # Random number of adults (between 1 and 5)
                    city=city,
                    country=country,
                    max_children=random.randint(0, 3),  # Random number of children (between 0 and 3)
                    iron_facilities=random.choice([True, False]),
                    tea_coffee_maker=random.choice([True, False]),
                    air_conditioning=random.choice([True, False]),
                    flat_screen_tv=random.choice([True, False]),
                    wake_up_service=random.choice([True, False]),
                    price_range_start=Decimal(price_range_start),
                    price_range_end=Decimal(price_range_end),
                    refundable=random.choice([True, False]),
                    availability_status=True  # All will be available
                )

            self.stdout.write(self.style.SUCCESS('Successfully created 20 random apartment types and assigned them to user with id=1'))

        except UserInfo.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with id=1 does not exist'))
