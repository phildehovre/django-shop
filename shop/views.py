from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, OrderItem, ProductTag, Order
from base.models import Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .helpers import calculations
from django.db.models import Q
from .forms import UpdateProductForm


def shop_view(request, selected_tags=None):
    page = "product_list"
    product_list = Product.objects.all()
    product_tags = ProductTag.objects.all()

    if request.method == "POST":
        selected_tags = request.POST.getlist("tag") if request.POST.getlist("tag") else ['all']
        search = request.POST.get('search')
        
        if selected_tags != ['all']:
            product_list = product_list.filter(tags__id__in=selected_tags)
        if search:
            product_list = product_list.filter(Q(name__contains=search) | Q(description__contains=search))

    edit_perm = False
    add_perm = False
    if request.user:
        edit_perm = request.user.has_perm('shop/change_product')
        add_perm = request.user.has_perm('shop/add_product')

    return render(
        request, 
        'shop/product_list.html', 
        {
            "products": product_list, 
            "tags": product_tags,
            "selected_tags": selected_tags,
            'page': page,
            "edit_perm": edit_perm,
            "add_perm": add_perm
        }
    )


@login_required
def add_to_basket(request, product):
    quantity = int(request.POST.get("quantity", 0))
    product = Product.objects.get(id=product.id)

    try:
        order = Order.objects.get(user=request.user, status=0)
    except Order.DoesNotExist:
        order = Order.objects.create(user=request.user, status=0)

    if quantity > product.stock:
        messages.error(request, "Not enough stock")
    else:
        product.stock -= quantity
        product.save()
        order_item = OrderItem.objects.create(product=product, quantity=quantity, order=order)
        messages.success(request, f"{product.name} ({quantity}) added to basket")
        
def product_detail(request, pk):    
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, id=pk)

    if request.method == "POST":
        add_to_basket(request, product)
         
    return render(request, 'shop/product_detail.html', {"product": product})

@login_required
def update_basket(request):
    order_id = request.POST.get("order_item_id")
    input_quantity = int(request.POST.get("quantity"))
    order_item = OrderItem.objects.get(id=order_id)
    product = order_item.product

    print("input:", input_quantity )

    diff = input_quantity - order_item.quantity
    print(f"Differential: {diff}")
    # Check if quantity is the same as order_item quantity
    # if so, return to basket
    if (order_item.quantity == input_quantity):
            return

        # Check stock
    if input_quantity > product.stock:
            messages.error(request, f"Not enough stock, {product.stock} left")
            return redirect("basket")
        
        # Check if quantity is greater than order quantity, 
        # updates as necessary
    if diff > 0:
            messages.success(request, f"{product.name}, {diff} added to basket")
    if diff < 0:
            messages.success(request, f"{product.name}, {abs(diff) } removed from basket")
        
    product.stock -= diff
    order_item.quantity += diff
    product.save()
    order_item.save()

def remove_from_basket(request):
    order_item_id = request.POST.get("order_item_id")
    order_item = OrderItem.objects.get(id=order_item_id)
    product = order_item.product
    product.stock += order_item.quantity
    product.save()
    order_item.delete()
    messages.success(request, f"{product.name} removed from basket")
    return redirect("basket")

def basket_view(request):
    """
    This view handles the basket page. 
    It allows users to view the items in their basket,
    update the quantity of items in their basket,
    and remove items from their basket.
    """
    page = 'basket'
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            remove_from_basket(request)
        else:
            update_basket(request)

    basket = OrderItem.objects.filter(Q(order__user=request.user), Q(order__status=0))

    return render(
         request, 
         'shop/basket.html', 
        {
            "basket": basket, 
            "total": calculations.calculate_total(basket),
            'page': page
        })

@login_required
def checkout_view(request):
    address_id = request.GET.get('address')
    page = 'checkout'
    order = Order.objects.get(user=request.user, status=0)
    basket = OrderItem.objects.filter(order__user=request.user, order=order)
    addresses = Address.objects.filter(user=request.user).order_by('-default')

    if len(addresses) == 0:
        messages.error(request, f"There are no shipping addresses, please enter your address in you account settings")

    if order.DoesNotExist:
         redirect('shop')

    if request.method == "POST":
        try:
            if address_id:
                address = Address.objects.get(id=address_id)
            else:
                address = Address.objects.filter(user=request.user, default=True).first()

            # Update order status
            order.status = 2
            order.shipping = address
            order.save()
            
            # Redirect to confirmation page
            page = 'confirmation'
        except Address.DoesNotExist:
            # Handle case when address doesn't exist
            messages.error(request, "Selected address does not exist.")
        except Exception as e:
            messages.error(request, f"There was an error: {str(e)}")

    return render(request, 'shop/checkout.html', {
        'basket': basket, 
        'total': calculations.calculate_total(basket),
        'page': page,
        'addresses': addresses,
        'order': basket
    })

@login_required
def add_product(request):
    page = 'add'

    if request.method == "POST":
        form = UpdateProductForm(request.POST, request.FILES)  # Instantiate the form with request data
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, f'Product was created successfully.')
            return redirect('shop')
        else:
            print(form.errors)
            messages.error(request, f"There was an error: Form is not valid.")
    else:
        form = UpdateProductForm()  # Instantiate an empty form for GET requests
    
    add_product_perm = request.user.has_perm('shop/add_product')
    print(add_product_perm)

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'shop/add_product.html', context)

@login_required
def edit_product(request, pk):
        page = 'edit'
        product = Product.objects.get(id=pk)
        if request.method == "POST":
            try:
                form = UpdateProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'{product.name} was updated succesfully.')
                    return redirect('shop')
            except Exception as e:
                messages.error(request, f"There was an error: {str(e)}")
        else:
            form = UpdateProductForm(instance=product)

        context = {
            'product': product,
            'page': page,
            'form': form
        }
        return render(request, 'shop/add_product.html', context)

