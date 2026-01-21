from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    country = models.CharField(max_length=100, default='India')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=20,
        choices=(('COD', 'Cash On Delivery'), ('ONLINE', 'Online Payment'))
    )

    status = models.CharField(
        max_length=20,
        choices=(('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled')),
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)

    discount_amount = models.DecimalField(
        max_digits=10,  
        decimal_places=2
    )

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class DeliveryCharge(models.Model):
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Minimum order amount for FREE delivery"
    )
    charge_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Delivery charge if order is below min amount"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Free above ₹{self.min_order_amount}"

