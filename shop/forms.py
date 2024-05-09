from django import forms
from django.contrib.auth.models import User
from .models import Product, ProductTag

class UpdateProductForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    tags = forms.ModelMultipleChoiceField(queryset=ProductTag.objects.all(), widget=forms.CheckboxSelectMultiple)
    stock = forms.IntegerField(min_value=0)
    price = forms.FloatField(min_value=0.01)
    

    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'tags', 'stock']