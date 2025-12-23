from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

# SHOW WISHLIST
def wishlist_detail(request):
    wishlist = request.session.get('wishlist', [])
    products = Product.objects.filter(id__in=wishlist)
    return render(request, 'wishlist/wishlist.html', {'products': products})


# ADD TO WISHLIST
def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')



def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    if product_id in wishlist:
        wishlist.remove(product_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')


   