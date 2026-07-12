from django.db import models


class Vehicle(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ON_TRIP = "ON_TRIP", "On Trip"
        IN_SHOP = "IN_SHOP", "In Shop"
        RETIRED = "RETIRED", "Retired"

    class VehicleType(models.TextChoices):
        TRUCK = "TRUCK", "Truck"
        VAN = "VAN", "Van"
        BIKE = "BIKE", "Bike"
        TRAILER = "TRAILER", "Trailer"
        CAR = "CAR", "Car"

    registration_number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, help_text="Vehicle Name/Model")
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices, default=VehicleType.VAN)
    max_load_capacity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    odometer_km = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    region = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registration_number} - {self.name}"

    def is_dispatchable(self):
        return self.status == self.Status.AVAILABLE
