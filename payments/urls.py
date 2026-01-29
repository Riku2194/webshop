from django.urls import path
from . import views

urlpatterns = [
    path("checkout/<int:product_id>/", views.create_checkout_session,name="checkout"),
]