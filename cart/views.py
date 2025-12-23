from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product


def cart_add(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1     
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')



def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        product.quantity = quantity
        product.subtotal = product.price * quantity
        total += product.subtotal
        products.append(product)

    return render(request, 'cart/cart.html', {
        'products': products,
        'total': total
    })



def cart_increase(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('cart_detail')



def cart_decrease(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart_detail')



def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart_detail')