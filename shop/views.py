from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def shop_view(request):
    """
    This view handles the shop page.
    """
    product_list = Product.objects.all()

    return render(request, 'shop/product_list.html', {"products": product_list})

@login_required
def add_to_basket(request, product):
    quantity = int(request.POST.get("quantity"))
    if quantity > product.stock:
        messages.error(request, "Not enough stock")
    else:
        order = Order.objects.create(user=request.user, product=product, quantity=quantity)
        product.stock -= quantity
        product.save()
        order.save()
        messages.success(request, f"{product.name} ({quantity}) added to basket")

def product_detail(request, product_id):    
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, id=product_id)

    if request.method == "POST":
        add_to_basket(request, product)
         
    return render(request, 'shop/product_detail.html', {"product": product})

@login_required
def update_basket(request):
    order_id = request.POST.get("order_id")
    input_quantity = int(request.POST.get("quantity"))
    order = Order.objects.get(id=order_id)
    product = order.product

    # Check if quantity is the same as order quantity
    # if so, return to basket
    validated_quantity = input_quantity

    if (order.quantity == input_quantity):
            return redirect("basket")

        # Check stock
    if input_quantity > product.stock:
            messages.error(request, f"Not enough stock, {product.stock} left")
            return redirect("basket")
        
        # Check if quantity is greater than order quantity, 
        # updates as necessary
    if input_quantity > order.quantity:
            validated_quantity = input_quantity - order.quantity
            messages.success(request, f"{product.name} {validated_quantity} added to basket")
    if input_quantity < order.quantity:
            validated_quantity = order.quantity - validated_quantity
            messages.success(request, f"{product.name} {validated_quantity } removed from basket")
        
    product.stock += validated_quantity
    order.quantity = validated_quantity
    product.save()
    order.save()

def remove_from_basket(request):
    order_id = request.POST.get("order_id")
    order = Order.objects.get(id=order_id)
    product = order.product
    product.stock += order.quantity
    product.save()
    order.delete()
    messages.success(request, f"{product.name} removed from basket")
    return redirect("basket")

def basket_view(request):
    """
    This view handles the basket page. 
    It allows users to view the items in their basket,
    update the quantity of items in their basket,
    and remove items from their basket.
    """
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            remove_from_basket(request)
        else:
            update_basket(request)

    basket = Order.objects.filter(user=request.user)

    return render(request, 'shop/basket.html', {"basket": basket})

