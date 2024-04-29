from django.shortcuts import render, redirect
from django.contrib import messages
from shop.models import Order, OrderItem
from base.forms import UpdateProfileForm
from base.models import Profile
from django.contrib.auth.decorators import login_required

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

    return render(request, 'account/account.html', {'page': page, 'account': profile, 'profile_form': profile_form})

def profile_view(request):
    page = 'profile'
    queryset = Profile.objects.filter(user=request.user)
    profile = queryset.first()
    print(profile.bio)

    return render(request, 'account/account.html', {'page': page, 'profile': profile})


def orders_view(request):

    orders = Order.objects.filter(user=request.user)

    order_list = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        if len(order_items) > 0:
            order_list.append(order_items.first())

    return render(request, 'account/orders.html', {'order_list': order_list})

def order_detail(request, order_id):
    if order_id:
        order = Order.objects.filter(id=order_id).first()

        
    return render(request, 'account/order_detail.html', {'order': order})


def settings_view(request):
    query = request.GET.get('q') if request.GET.get('q') != None else 'view'
    page= query
    profile = Profile.objects.filter(user=request.user).first()

    profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

    if request.method == "POST":
        try:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was updated successfully.')
                return redirect('profile')
        except Exception as e:
            messages.error(request, f"There was an error: {str(e)}")

    return render(request, 'account/settings.html' , {'profile': profile, 'profile_form': profile_form, 'page': page})