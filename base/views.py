from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile
from .forms import UpdateProfileForm

# Create your views here.

def base_view(request):
    return render(request, 'base/base.html')

def about_view(request):
    return render(request, 'base/about.html')


def login_view(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successully logged in!')
                # if profile is None:
                #     profile = Profile.objects.create(user=request.user)
                #     profile.save()
                return redirect('shop')
        except:
            messages.error(request, 'Username or password incorrect')   
            return redirect('home')

    return render(request, 'base/login_register.html', {'page': page})


def user_logout(request):
    logout(request)
    return redirect('home')

def user_register(request):
    page = 'register'

    if request.method == "POST":
        try:
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
                return redirect('shop')
        except Exception as e: 
            messages.error(request,f'An error occurred during registration: {str(e)}')
    else:
        form = UserCreationForm()
        
    return render(request, "base/login_register.html", {'page': page, "form": form})

