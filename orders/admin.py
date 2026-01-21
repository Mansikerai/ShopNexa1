from django.contrib import admin
from .models import Order, OrderItem, Coupon, DeliveryCharge

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'final_amount', 'status', 'created_at')
    readonly_fields = ('final_amount', 'discount_amount', 'delivery_charge')

admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(DeliveryCharge)