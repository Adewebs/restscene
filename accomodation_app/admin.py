from django.contrib import admin
from .models import ApartmentType, Booking,ApartmentMedia

class ApartmentMediaInline(admin.TabularInline):
    model = ApartmentMedia
    extra = 1  # Number of empty media fields to show by default in the admin interface

class ApartmentTypeAdmin(admin.ModelAdmin):
    inlines = [ApartmentMediaInline]

admin.site.register(ApartmentType, ApartmentTypeAdmin)
admin.site.register(ApartmentMedia)
admin.site.register(Booking)