from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def shop_view(request):

    product_list = Product.objects.all()

    return render(request, 'shop/product_list.html', {"products": product_list})

@login_required
def select_or_create_basket(request):
    basket = Basket.objects.filter(user=request.user)
    if basket.exists():
        return basket.first()
    else:
        basket = Basket.objects.create(user=request.user)
        basket.save()
        return basket

@login_required
def add_to_basket(request, product):
    quantity = int(request.POST.get("quantity"))
    if quantity > product.stock:
        messages.error(request, "Not enough stock")
    else:
        basket = select_or_create_basket(request)
        basket.products.add(product)
        
        product.stock -= quantity
        product.save()
        basket.save()
        messages.success(request, f"{product.name} ({quantity}) added to basket")

def product_detail(request, product_id):    
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, id=product_id)

    if request.method == "POST":
        add_to_basket(request, product)
         
    return render(request, 'shop/product_detail.html', {"product": product})

def basket_view(request):
    basket = select_or_create_basket(request)
    products = basket.products.all()
    return render(request, 'shop/basket.html', {"basket": basket, "products": products})