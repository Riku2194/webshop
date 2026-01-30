from django.urls import path
from . import views

urlpatterns = [
    path("download/<str:signed_value>/", views.download_material, name="download"),
]