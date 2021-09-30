from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Authentication Form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Forms and Models
from App_Login.models import Profile, SellerInfo
from App_Login.forms import ProfileForm, SellerInfoForm, SignUpForm

# Create your views here.


def sign_up(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/signup.html', context={'form': form})


def login_page(request):
    form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request, 'App_Login/login.html', context={'form': form})


def logout_page(request):
    logout(request)
    messages.warning(request, 'You are logged out!')
    return HttpResponseRedirect(reverse('App_Shop:home'))


@login_required
def profile(request):
    return render(request, 'App_Login/profile.html', context={})


@login_required
def edit_profile(request):
    current_user_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=current_user_profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=current_user_profile)
        if form.is_valid():
            form.save()
            form = ProfileForm(instance=current_user_profile)
            messages.success(request, 'Changes saved!')
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/change_profile.html', context={'form': form})


def seller_signup(request):
    form = SignUpForm
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)

        form = SignUpForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            user_obj.is_seller = True
            user_obj.save()
            seller_info = SellerInfo(user=user_obj)
            seller_info.save()
            print(user_obj.is_seller)
            messages.success(request, 'Login into your seller account')
            return HttpResponseRedirect(reverse('App_Login:seller-login'))

    return render(request, 'App_Login/seller_signup.html', context={'form': form})


def seller_login(request):
    form = AuthenticationForm
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'seller successfully logged in!')
                return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request, 'App_Login/seller_login.html', context={'form': form})


@login_required
def seller_profile(request):
    return render(request, 'App_Login/seller_profile.html', context={})


@login_required
def edit_seller_profile(request):
    current_user_profile = Profile.objects.get(user=request.user)
    current_user_seller_info = SellerInfo.objects.get(user=request.user)

    form = ProfileForm(instance=current_user_profile)
    seller_info_form = SellerInfoForm(instance=current_user_seller_info)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=current_user_profile)
        seller_info_form = SellerInfoForm(request.POST, instance=current_user_seller_info)

        if form.is_valid() and seller_info_form.is_valid():
            form.save()
            seller_info_form.save()
            form = ProfileForm(instance=current_user_profile)
            seller_info_form = SellerInfoForm(instance=current_user_seller_info)
            messages.success(request, 'Changes saved!')
            return HttpResponseRedirect(reverse('App_Login:seller-profile'))
    return render(request, 'App_Login/change_seller_profile.html', context={'form': form, 'seller_info_form': seller_info_form})
