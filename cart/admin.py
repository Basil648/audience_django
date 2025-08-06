from django.contrib import admin
from .models import BillingDetails

@admin.register(BillingDetails)
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_address', 'get_cart_items_pretty', 'payment_method', 'created_at')
    readonly_fields = ('get_cart_items_pretty',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Customer Name'

    def get_cart_items_pretty(self, obj):
        items = obj.cart_items
        if not items:
            return "-"
        return "\n".join([f"{item['quantity']} x {item['product_name']} @ ₹{item['price']}" for item in items])
    get_cart_items_pretty.short_description = 'Ordered Products'
