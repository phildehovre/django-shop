from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Create your views here.

def shop_view(request):

    product_list = Product.objects.all()

    return render(request, 'shop/product_list.html', {"products": product_list})


def product_detail(request, product_id):    
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, id=product_id)

    return render(request, 'shop/product_detail.html', {"product": product})