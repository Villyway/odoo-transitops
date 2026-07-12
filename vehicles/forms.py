from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["registration_number", "name", "vehicle_type", "max_load_capacity_kg",
                  "odometer_km", "acquisition_cost", "region", "status"]
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in
                   ["registration_number", "name", "region"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in self.Meta.widgets:
                field.widget.attrs.update({"class": "form-select" if isinstance(field.widget, forms.Select) else "form-control"})
