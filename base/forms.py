from django import forms

from django.contrib.auth.models import User
from .models import Profile, Address

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class UpdateAddressForm(forms.ModelForm):
    address=forms.CharField(max_length=200)
    city=forms.CharField(max_length=200)
    postcode=forms.CharField(max_length=100)
    country=forms.CharField(max_length=200)
    additional=forms.Textarea()

    class Meta:
        model = Address
        fields = ['name', 'address', 'city', 'postcode', 'country', 'additional', 'default']