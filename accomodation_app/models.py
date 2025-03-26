from django.db import models
from auth_app.models import UserInfo

class ApartmentType(models.Model):

    APARTMENT_CHOICES = [
        ('featured', 'Featured'),
        ('master_suite', 'Master Suite'),
        ('mini_suite', 'Mini Suite'),
        ('ultra_deluxe', 'Ultra Deluxe'),
        ('luxury_room', 'Luxury Room'),
        ('premium_room', 'Premium Room'),
        ('normal_room', 'Normal Room'),
    ]

    name = models.CharField(max_length=100, choices=APARTMENT_CHOICES, default="featured")
    host = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Rating out of 5
    max_adults = models.IntegerField(default=1)
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


    def __str__(self):
        return self.name

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

    def __str__(self):
        return f"Booking by {self.guest} for {self.apartment_type.name}"

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
