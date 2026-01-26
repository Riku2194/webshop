from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "purchase_price")
    list_filter = ("order",)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)