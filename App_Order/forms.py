from django import forms
from App_Order.models import Coupon


class CouponForm(forms.Form):
    code = forms.CharField(max_length=50, label='Coupon Code', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
