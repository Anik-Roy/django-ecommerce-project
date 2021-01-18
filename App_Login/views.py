from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Authentication Form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Forms and Models
from App_Login.models import Profile
from App_Login.forms import ProfileForm, SignUpForm

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
