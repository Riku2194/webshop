from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    search_fields = ("name", )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
