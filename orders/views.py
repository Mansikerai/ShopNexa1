from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from cart.models import Cart, CartItem
from .models import Order, OrderItem


@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return redirect('cart_detail')

    total = sum(item.subtotal() for item in items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            country=request.POST['country'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            payment_method=request.POST['payment_method'],
            total_amount=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        items.delete()  
        return redirect('order_success')

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required(login_url='login')
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    return render(request, "orders/order_summary.html", {
        "order": order,
        "items": items
    })

def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    order = Order.objects.create(user=request.user)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_price=item.product.price,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )

        # reduce stock
        item.product.stock -= item.quantity
        if item.product.stock <= 0:
            item.product.is_active = False
        item.product.save()

    cart_items.delete()
