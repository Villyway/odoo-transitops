from django.db import models
from django.core.exceptions import ValidationError
from vehicles.models import Vehicle
from drivers.models import Driver


class Trip(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        DISPATCHED = "DISPATCHED", "Dispatched"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    source = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="trips")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="trips")
    cargo_weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    planned_distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    final_odometer_km = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fuel_consumed_liters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Trip #{self.id}: {self.source} -> {self.destination}"

    def clean(self):
        if self.cargo_weight_kg and self.vehicle_id:
            if self.cargo_weight_kg > self.vehicle.max_load_capacity_kg:
                raise ValidationError(
                    f"Cargo Weight ({self.cargo_weight_kg} kg) exceeds vehicle's "
                    f"maximum load capacity ({self.vehicle.max_load_capacity_kg} kg)."
                )

    def actual_distance_km(self):
        if self.final_odometer_km and self.vehicle:
            return self.final_odometer_km - (self.vehicle.odometer_km or 0)
        return None
