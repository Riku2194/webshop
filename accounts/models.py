from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birthday = models.DateField(
        null=True, blank=True, verbose_name="誕生日"
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Stripe顧客ID"
    )

    def __str__(self):
        return self.username
