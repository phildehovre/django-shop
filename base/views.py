from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import UpdateUserForm, UpdateProfileForm
from django.db.models import Q

# Create your views here.

def home_view(request):
    print("rendering home: ", request)
    return render(request, 'base/base.html')

def about_view(request):
    print("rendering about: ", request)
    return render(request, 'base/about.html')

def account_view(request):
    #https://dev.to/earthcomfy/django-user-profile-3hik
    profile_form = UpdateProfileForm(request.POST, instance=request.user)
    user_form = UpdateUserForm(request.POST,request.FILES, instance=request.user.profile)

    return render(request, 'base/account.html', {"profile_form": profile_form, "user_form": user_form})

def login_view(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.error(request, 'Successully logged in!')
                
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
            return redirect('home')
        else: 
            messages.error(request,'An error occurred during registration, please try again')
        
    return render(request, "base/login_register.html", {'page': page, "form": form})