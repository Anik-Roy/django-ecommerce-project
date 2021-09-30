from django.urls import path
from App_Shop import views

app_name = 'App_Shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('add-product/', views.AddProduct.as_view(), name='add_product'),
    path('update-product/<pk>/', views.UpdateProduct.as_view(), name='update_product'),
    path('my-products/', views.SellerOwnProduct.as_view(), name='my-product'),
]
