from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect('checkout')

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        total += product.price * qty

    order = Order.objects.create(
        user=request.user,
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        phone=request.POST['phone'],
        country=request.POST['country'],
        state=request.POST['state'],
        city=request.POST['city'],
        address=request.POST['address'],
        payment_method=request.POST['payment_method'],
        total_amount=total,
        status='Pending'
    )

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=product.price
        )

    # request.session['cart'] = {}  # clear cart

    return redirect('order_success')


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def dummy_payment(request):
    return redirect('order_success')