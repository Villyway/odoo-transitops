from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "name", "vehicle_type", "status", "region", "max_load_capacity_kg")
    list_filter = ("status", "vehicle_type", "region")
    search_fields = ("registration_number", "name")
