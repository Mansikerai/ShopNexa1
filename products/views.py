from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get('category')
    query = request.GET.get('q')   

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'query': query
    })
from django.shortcuts import get_object_or_404

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {
        "products": products
    })

