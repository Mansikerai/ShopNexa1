from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category__id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })
from django.shortcuts import get_object_or_404

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

