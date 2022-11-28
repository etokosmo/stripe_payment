from django.contrib import admin
from django.utils.html import format_html

from .models import Item, Order, OrderElements


class OrderElementsInline(admin.TabularInline):
    model = OrderElements
    readonly_fields = ["price_in_order"]
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description",
                    "price", "get_preview"]
    readonly_fields = ["get_preview"]

    def get_preview(self, image):
        if image.image:
            return format_html(
                "<img src={} style='max-height: 200px;'>",
                image.image.url
            )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderElementsInline]
    list_display = ["customer_firstname", "customer_lastname",
                    "customer_address", "registrated_at"]


@admin.register(OrderElements)
class OrderElementsAdmin(admin.ModelAdmin):
    raw_id_fields = ["order", "item"]
    list_display = ["order", "item", "quantity", "price_in_order",
                    "get_item_price"]
    readonly_fields = ["price_in_order"]

    def save_model(self, request, obj, form, change):
        obj.price_in_order = obj.item.price
        obj.save()
        super().save_model(request, obj, form, change)

    def get_item_price(self, obj):
        return obj.get_item_price()
