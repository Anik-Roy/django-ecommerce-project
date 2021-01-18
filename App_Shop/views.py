from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView

# models
from App_Shop.models import Product

# mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Home(ListView):
    context_object_name = 'products'
    model = Product
    template_name = 'App_Shop/home.html'


class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product
    template_name = 'App_Shop/product_detail.html'
