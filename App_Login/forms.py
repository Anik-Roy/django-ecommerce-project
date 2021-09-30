from django import forms
from App_Login.models import User, Profile, SellerInfo
from django.contrib.auth.forms import UserCreationForm

# Forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'col': 10})
        }


class SellerInfoForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        exclude = ('user', )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

