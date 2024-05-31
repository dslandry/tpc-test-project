from django.contrib import admin

from .models import Order, Product, Profile


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
    search_fields = ("name",)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "product__name")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "phone_number", "date_of_birth")
    search_fields = ("user__username", "phone_number")


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
