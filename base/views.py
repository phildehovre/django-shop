from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Profile
from .forms import UpdateProfileForm

# Create your views here.

def home_view(request):
    print("rendering home: ", request)
    return render(request, 'base/base.html')

def about_view(request):
    print("rendering about: ", request)
    return render(request, 'base/about.html')

def account_view(request):
    queryset = Profile.objects.filter(user=request.user)
    profile = queryset.first()

    form = UpdateProfileForm(instance=profile)

    return render(request, 'base/account.html', {'profile': profile, 'form': form})

def profile_view(request):
    queryset = Profile.objects.filter(user=request.user)
    profile = queryset.first()

    return render(request, 'base/account.html', {'profile': profile})

def login_view(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            profile = Profile.objects.filter(user=request.user)
            if user is not None:
                if profile is None:
                    profile = Profile.objects.create(user=request.user)
                    profile.save(commit=False)
                login(request, user)
                messages.success(request, 'Successully logged in!')
                return redirect('shop/products')
        except:
            messages.error(request, 'Username or password incorrect')   

    return render(request, 'base/login_register.html', {'page': page})


def user_logout(request):
    logout(request)
    return redirect('home')

def user_register(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # The commit=False argument passed to the save() method 
            # indicates that the changes made to the user instance 
            # should not be immediately saved to the database. 
            # This allows additional modifications to be made 
            # to the user instance before it's saved permanently.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            # It is crucial to initiate profile creation
            # AFTER the user was saved AND logged in.
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('shop/products')
        else: 
            messages.error(request,'An error occurred during registration, please try again')
        
    return render(request, "base/login_register.html", {'page': page, "form": form})