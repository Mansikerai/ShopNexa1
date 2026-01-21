from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from users.models import Address
from .models import Order, OrderItem, Coupon, DeliveryCharge


@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return redirect('cart_detail')


    subtotal = sum(item.product.price * item.quantity for item in items)


    delivery_charge = Decimal("0")
    delivery_rule = DeliveryCharge.objects.filter(is_active=True).first()

    if delivery_rule and subtotal < delivery_rule.min_order_amount:
        delivery_charge = delivery_rule.charge_amount


    discount = Decimal("0")
    coupon = None
    coupon_error = ""

    billing = {
        "first_name": request.POST.get("first_name", ""),
        "last_name": request.POST.get("last_name", ""),
        "email": request.POST.get("email", ""),
        "phone": request.POST.get("phone", ""),
        "country": request.POST.get("country", "India"),
        "address": request.POST.get("address", ""),
        "city": request.POST.get("city", ""),
        "state": request.POST.get("state", ""),
    }

 
    if request.method == "POST" and "apply_coupon" in request.POST:
        coupon_code = request.POST.get("coupon_code", "").strip()

        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)

            if subtotal >= coupon.min_order_amount:
                discount = coupon.discount_amount
            else:
                discount = Decimal("0")
                coupon_error = f"Coupon valid only for orders above ₹{coupon.min_order_amount}"

        except Coupon.DoesNotExist:
            discount = Decimal("0")
            coupon_error = "Invalid coupon code"


    final_amount = subtotal + delivery_charge - discount


    if request.method == "POST" and "place_order" in request.POST:

        # Re-validate coupon for security
        coupon_code = request.POST.get("coupon_code", "").strip()
        discount = Decimal("0")

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if subtotal >= coupon.min_order_amount:
                    discount = coupon.discount_amount
            except Coupon.DoesNotExist:
                discount = Decimal("0")

        final_amount = subtotal + delivery_charge - discount

        address = Address.objects.create(
            user=request.user,
            full_name=f"{billing['first_name']} {billing['last_name']}",
            phone=billing["phone"],
            address_line=billing["address"],
            city=billing["city"],
            state=billing["state"],
            country=billing["country"],
        )

        order = Order.objects.create(
            user=request.user,
            first_name=billing["first_name"],
            last_name=billing["last_name"],
            email=billing["email"],
            phone=billing["phone"],
            country=billing["country"],
            address=billing["address"],
            city=billing["city"],
            state=billing["state"],
            payment_method=request.POST.get("payment_method", "COD"),
            subtotal=subtotal,
            discount_amount=discount,
            delivery_charge=delivery_charge,
            final_amount=final_amount,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

            item.product.stock -= item.quantity
            if item.product.stock <= 0:
                item.product.is_active = False
            item.product.save()

        items.delete()
        return redirect("order_summary", order_id=order.id)


    return render(request, "orders/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "final_amount": final_amount,
        "coupon": coupon,
        "coupon_error": coupon_error,
        "billing": billing,
    })


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required(login_url='login')
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_summary.html", {
        "order": order,
        "items": order.items.all(),
    })

@login_required(login_url='login')
def order_success(request):
    return render(request, "orders/order_success.html")