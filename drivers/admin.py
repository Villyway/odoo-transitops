from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "license_number", "license_expiry_date", "status", "safety_score")
    list_filter = ("status", "license_category")
    search_fields = ("name", "license_number")
