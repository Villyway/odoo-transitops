from . import views
from django.urls import path

app_name = "fuel"

urlpatterns = [
    path("", views.fuel_list, name="list"),
    path("add/", views.fuel_create, name="add"),
]
