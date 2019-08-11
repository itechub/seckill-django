from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Activity, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "price",
        "inventory",
        "created",
    )
    readonly_fields = ("id", "created")


class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "start_time", "end_time")
    readonly_fields = ("id", "created")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "activity", "payment", "created")
    readonly_fields = ("id", "created")


admin.site.register(Product, ProductAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Order, OrderAdmin)
