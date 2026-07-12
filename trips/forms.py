from django import forms
from .models import Trip
from vehicles.models import Vehicle
from drivers.models import Driver


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["source", "destination", "vehicle", "driver", "cargo_weight_kg", "planned_distance_km", "revenue"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vehicle"].queryset = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE)
        self.fields["driver"].queryset = Driver.objects.filter(status=Driver.Status.AVAILABLE)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-select" if isinstance(field.widget, forms.Select) else "form-control"})

    def clean(self):
        cleaned = super().clean()
        vehicle = cleaned.get("vehicle")
        driver = cleaned.get("driver")
        cargo = cleaned.get("cargo_weight_kg")

        if vehicle and cargo is not None and cargo > vehicle.max_load_capacity_kg:
            raise forms.ValidationError(
                f"Cargo Weight ({cargo} kg) exceeds vehicle's maximum load capacity "
                f"({vehicle.max_load_capacity_kg} kg)."
            )
        if vehicle and not vehicle.is_dispatchable():
            raise forms.ValidationError("Selected vehicle is not available for dispatch.")
        if driver and not driver.is_dispatchable():
            raise forms.ValidationError("Selected driver is not available (license expired/suspended/on trip).")
        return cleaned


class TripCompleteForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["final_odometer_km", "fuel_consumed_liters"]
        widgets = {
            "final_odometer_km": forms.NumberInput(attrs={"class": "form-control"}),
            "fuel_consumed_liters": forms.NumberInput(attrs={"class": "form-control"}),
        }
