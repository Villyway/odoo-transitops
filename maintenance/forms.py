from django import forms
from .models import MaintenanceLog
from vehicles.models import Vehicle


class MaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ["vehicle", "title", "description", "cost"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vehicle"].queryset = Vehicle.objects.exclude(status=Vehicle.Status.RETIRED)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-select" if isinstance(field.widget, forms.Select) else "form-control"})
