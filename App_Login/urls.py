from django.urls import path
from App_Login import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('seller-signup/', views.seller_signup, name='seller-signup'),
    path('seller-login/', views.seller_login, name='seller-login'),
    path('seller-profile/', views.seller_profile, name='seller-profile'),
    path('edit-seller-profile/', views.edit_seller_profile, name='edit-seller-profile'),
]
