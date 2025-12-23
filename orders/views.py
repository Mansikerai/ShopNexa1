from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

  
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_amount=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear cart after order
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success')

    # GET request → show checkout page
    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
         