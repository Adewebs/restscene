import geoip2.database
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import os


class GeoIPMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

        # Construct the absolute path to the GeoIP2 database
        geoip2_db_path = os.path.join(settings.BASE_DIR, 'geoip2', 'GeoLite2-Country.mmdb')

        # Initialize the GeoIP2 reader with the correct file path
        self.geoip_reader = geoip2.database.Reader(geoip2_db_path)

    def __call__(self, request):
        # First check if the 'HTTP_X_FORWARDED_FOR' header exists
        ip = request.META.get('HTTP_X_FORWARDED_FOR')

        if not ip:  # Fallback to REMOTE_ADDR if not present
            ip = request.META.get('REMOTE_ADDR')

        if ip:
            try:
                # Look up the IP address to get the country information
                response = self.geoip_reader.country(ip)
                country_code = response.country.iso_code
                request.session['user_country'] = country_code  # Store country in session
            except geoip2.errors.AddressNotFoundError:
                request.session['user_country'] = None  # Handle case where IP address is not found
        return self.get_response(request)

