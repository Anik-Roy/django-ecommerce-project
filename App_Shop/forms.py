from django import forms
from App_Shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user', )
