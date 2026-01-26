from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "stripe_customer_id", "is_active")
    search_fields = ("username", "email", "stripe_customer_id")

admin.site.register(CustomUser, CustomUserAdmin)