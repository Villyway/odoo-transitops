from django.urls import path
from . import views

app_name = "fuel"

urlpatterns = [
    path("", views.fuel_list, name="list"),
    path("add/", views.fuel_create, name="add"),
]
