from django.core.management.base import BaseCommand
from django.conf import settings
from accomodation_app.models import ApartmentType, Booking


class Command(BaseCommand):
    help = 'Update the currency field for both ApartmentType and Booking models based on the selected country.'

    def handle(self, *args, **kwargs):
        # Update currency for ApartmentType where country is set and currency is not set
        self.update_apartment_type_currency()

        # Update currency for Booking where country is set and currency is not set
        self.update_booking_currency()

    def update_apartment_type_currency(self):
        # Get all apartment types that have a country set but no currency set
        apartment_types = ApartmentType.objects.filter(country__isnull=False, currency__isnull=True)

        updated_count = 0
        for apartment in apartment_types:
            currency = settings.COUNTRY_CURRENCY_MAPPING.get(apartment.country)
            if currency:
                apartment.currency = currency
                apartment.save()
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} ApartmentType records with currency.'))

    def update_booking_currency(self):
        # Get all bookings that have a country set but no currency set
        bookings = Booking.objects.filter(country__isnull=False, currency__isnull=True)

        updated_count = 0
        for booking in bookings:
            currency = settings.COUNTRY_CURRENCY_MAPPING.get(booking.country)
            if currency:
                booking.currency = currency
                booking.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} Booking records with currency.'))
