from django import forms
from .models import Driver


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["name", "license_number", "license_category", "license_expiry_date",
                  "contact_number", "safety_score", "status"]
        widgets = {"license_expiry_date": forms.DateInput(attrs={"type": "date", "class": "form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "license_expiry_date":
                field.widget.attrs.update({"class": "form-select" if isinstance(field.widget, forms.Select) else "form-control"})
