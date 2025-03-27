from django.db import models
from auth_app.models import UserInfo
from django.conf import settings

COUNTRY_CHOICES = settings.COUNTRY_CHOICES
CURRENCY_CHOICES = settings.CURRENCY_CHOICES
class ApartmentType(models.Model):

    APARTMENT_CHOICES = [
        ('Featured', 'featured'),
        ('Master Suite', 'Master Suite'),
        ('Mini Suite', 'Mini Suite'),
        ('Ultra Deluxe', 'Ultra Deluxe'),
        ('Luxury Room', 'Luxury Room'),
        ('Premium Room', 'Premium Room'),
        ('Normal Room', 'Normal Room'),
    ]

    name = models.CharField(max_length=100, choices=APARTMENT_CHOICES, default="featured")
    host = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Rating out of 5
    max_adults = models.IntegerField(default=1)
    city =models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=3,choices=COUNTRY_CHOICES,blank=True,null=True)
    max_children = models.IntegerField(default=0)
    iron_facilities = models.BooleanField(default=False)
    tea_coffee_maker = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    flat_screen_tv = models.BooleanField(default=False)
    wake_up_service = models.BooleanField(default=False)
    price_range_start = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_end = models.DecimalField(max_digits=10, decimal_places=2)
    refundable = models.BooleanField(default=True)
    availability_status = models.BooleanField(default=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True, null=True)
    def save(self, *args, **kwargs):
        # Automatically set the currency based on the selected country
        if self.country and not self.currency:  # Only set currency if it's not already set
            self.currency = settings.COUNTRY_CURRENCY_MAPPING.get(self.country)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} -  {self.country}"



    class Meta:
        verbose_name = 'Apartment Type'
        verbose_name_plural = 'Apartment Types'


class ApartmentMedia(models.Model):
    """Model for storing images and videos related to an apartment."""

    apartment = models.ForeignKey(ApartmentType, related_name="media", on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='apartment_media/%Y/%m/%d/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description for the media

    def __str__(self):
        return f"{self.media_type.capitalize()} for {self.apartment.name}"

    class Meta:
        verbose_name = 'Apartment Media'
        verbose_name_plural = 'Apartment Media'


class Booking(models.Model):

    """Model for user bookings."""
    guest = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    apartment_type = models.ForeignKey(ApartmentType, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    checkin_date = models.DateTimeField()
    checkin_out_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=3,choices=COUNTRY_CHOICES,blank=True,null=True)
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    message = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically set the currency based on the selected country
        if self.country and not self.currency:  # Only set currency if it's not already set
            self.currency = settings.COUNTRY_CURRENCY_MAPPING.get(self.country)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.guest} for {self.apartment_type.name}"

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


class ApartmentReviews(models.Model):
    reviewer = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    apartment_type = models.ForeignKey(ApartmentType, on_delete=models.CASCADE)
    reviewer_comment = models.CharField(max_length=755,blank=True,null=True)
    reviewers_down_rate = models.IntegerField(default=0)
    reviewers_up_rating = models.IntegerField(default=0)