from django import forms
from .models import FuelLog


class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ["vehicle", "liters", "cost", "date", "notes"]
        widgets = {"date": forms.DateInput(attrs={"type": "date", "class": "form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "date":
                field.widget.attrs.update({"class": "form-select" if isinstance(field.widget, forms.Select) else "form-control"})
