from django.shortcuts import render, redirect
from django.contrib import messages
from shop.models import Order, OrderItem
from base.forms import UpdateProfileForm, UpdateAddressForm
from base.models import Profile, Address
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def account_view(request):
    page = 'account'
    queryset = Profile.objects.filter(user=request.user)
    profile = queryset.first()

    profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

    if request.method == "POST":
        try:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was updated successfully.')
                return redirect('profile')
        except Exception as e:
            messages.error(request, f"There was an error: {str(e)}")

    user = request.user
    print(user.has_perm( 'shop.add_product'))

    return render(request, 'account/account.html', {'page': page, 'account': profile, 'profile_form': profile_form})

def profile_view(request):
    page = 'profile'
    queryset = Profile.objects.filter(user=request.user)
    profile = queryset.first()
    print(profile.bio)

    return render(request, 'account/account.html', {'page': page, 'profile': profile})


def orders_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status=0)
    items_array = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        if len(order_items) > 0:
            items_array.append(order_items)

    return render(request, 'account/orders.html', 
                  {
                      'order_items': items_array,
                      'orders': orders
                })

def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=order)
        
    return render(request, 'account/order_detail.html', 
                  {
                    'order': order, 
                    'order_items': order_items
                   })


def settings_view(request):
    """
    Handles address creation and profile updates.
    The address CRUD operations are handled via a URL 'q' parameter.
    Assigned to the variable 'page' this quickly switches between 
    differents settings and operations.
    """
    query = request.GET.get('q') if request.GET.get('q') != None else 'view'
    page= query
    profile = Profile.objects.filter(user=request.user).first()
    profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)


    if request.method == "POST" and page == 'edit':
        try:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was updated successfully.')
                return redirect('settings')
        except Exception as e:
            messages.error(request, f"There was an error: {str(e)}")
    else:
            profile_form = UpdateProfileForm(instance=profile)



    addresses = Address.objects.filter(user=request.user).order_by('-default')
    address_form = UpdateAddressForm()

    if page == 'address':
        address_id = request.GET.get('id')
        address = None
        if address_id:
            try:
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                pass

        if request.method == 'POST':
            address_form = UpdateAddressForm(request.POST, instance=address)
            try:
                if address_form.is_valid():
                    address = address_form.save(commit=False)
                    address.user = request.user 
                    address.save()
                    return redirect('settings')
            except Exception as e:
                messages.error(request, f"There was an error: {str(e)}")
        else:
            # Initialize the form with the address instance
            address_form = UpdateAddressForm(instance=address)

       

    return render(request, 
                  'account/settings.html' , 
                  {
                    'profile': profile, 
                    'profile_form': profile_form, 
                    'page': page,
                    'addresses': addresses,
                    'address_form': address_form
                })

def delete_address(request, pk):
    address = Address.objects.get(id=pk)

    if request.method == 'POST':
        address.delete()
        return redirect('settings')
    return render(request, 'account/delete_address.html', {'address': address})

def set_default(request, pk):
    address=Address.objects.get(id=pk)

    if address != None:
        address.default = True
        address.save()
        return redirect('settings')
    
    return render(request, 'account/settings.html')

def payment_methods(request):

    return render(request, 'account/payment_methods.html', {})

def security_view(request):
    
    return render(request, 'account/security.html')