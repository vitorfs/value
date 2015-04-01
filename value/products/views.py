from django.shortcuts import render

def products(request):
    return render(request, 'products/products.html')

def product(request, product_id):
    return render(request, 'products/product.html')
