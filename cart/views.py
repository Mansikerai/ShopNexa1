from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem

@login_required(login_url='login')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()

    return redirect('cart_detail')


@login_required(login_url='login')
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.subtotal() for item in items)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })



@login_required(login_url='login')
def cart_increase(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_detail')


@login_required(login_url='login')
def cart_decrease(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_detail')


@login_required(login_url='login')
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')