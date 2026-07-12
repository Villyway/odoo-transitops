from django.contrib import admin
from .models import FuelLog


@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "liters", "cost", "date")
    list_filter = ("date",)
