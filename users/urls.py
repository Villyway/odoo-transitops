from django.urls import path
from .views import TransitLoginView, TransitLogoutView, signup_view

app_name = "users"

urlpatterns = [
    path("login/", TransitLoginView.as_view(), name="login"),
    path("logout/", TransitLogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
]
