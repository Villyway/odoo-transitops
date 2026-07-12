from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.Role.choices)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "role", "phone", "password1", "password2")
