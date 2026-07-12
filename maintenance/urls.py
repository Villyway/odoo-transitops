from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("", views.maintenance_list, name="list"),
    path("add/", views.maintenance_create, name="add"),
    path("<int:pk>/close/", views.maintenance_close, name="close"),
]
