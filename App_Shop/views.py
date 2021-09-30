from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse

from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

# models
from App_Shop.models import Product
from App_Shop.forms import ProductForm

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


class SellerOwnProduct(ListView):
    context_object_name = 'products'
    template_name = 'App_Shop/seller_own_products.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class AddProduct(CreateView):
    context_object_name = 'form'
    template_name = 'App_Shop/add_product.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddProduct, self).form_valid(form)

    def get_success_url(self):
        return reverse('App_Shop:product_detail', kwargs={'pk': self.object.pk})


class UpdateProduct(UpdateView):
    context_object_name = 'form'
    template_name = 'App_Shop/update_product.html'
    model = Product
    fields = ('mainimage', 'name', 'category', 'preview_text', 'detail_text', 'price', 'old_price', 'in_stock', )

    def get_success_url(self):
        return reverse('App_Shop:product_detail', kwargs={'pk': self.object.pk})
