from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from App_Order.models import Cart, Order, Coupon
from App_Order.forms import CouponForm
from App_Payment.models import BillingAddress
from App_Payment.forms import BillingAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingAddressForm(instance=saved_address)
    coupon_form = CouponForm
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, 'Shipping address saved!')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    order = order_qs[0]
    order_items = order.orderitems.all()
    print(order_items)
    order_total = order.get_totals()
    print(order_total)
    order_total_without_discount = order.get_totals_without_discount()
    order_discount_amount = order.get_discount_amount()
    return render(request, 'App_Payment/checkout.html', context={'form': form, 'coupon_form': coupon_form,
                                                                 'order': order,
                                                                 'order_total_without_discount': order_total_without_discount,
                                                                 'order_discount_amount': order_discount_amount,
                                                                 'order_items': order_items,
                                                                 'order_total': order_total,
                                                                 'saved_address': saved_address})


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f'Please complete shipping address!')
        return redirect('App_Payment:checkout')
    if not request.user.profile.is_fully_field():
        messages.info(request, f'Please complete your profile information!')
        return redirect('App_Login:edit-profile')

    store_id = 'abcco60031a1f48704'
    api_key = 'abcco60031a1f48704@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                            sslc_store_pass=api_key)
    status_url = request.build_absolute_uri(reverse('App_Payment:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='mixed',
                                      product_name=order_items, num_of_item=order_items_count, shipping_method='Courier',
                                      product_profile='None')

    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email,
                                address1=current_user.profile.address, address2=current_user.profile.address,
                                city=current_user.profile.city, postcode=current_user.profile.zipcode,
                                country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address,
                                city=saved_address.city, postcode=saved_address.zipcode,
                                country=saved_address.country)
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, f'Your payment completed successfully! Please will be redirected after 5 sec!')
            return HttpResponseRedirect(reverse('App_Payment:purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request, f'Your payment failed! Try again! Please will be redirected after 5 sec!')
    return render(request, 'App_Payment/complete.html', context={})


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('App_Shop:home'))


@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
        return render(request, 'App_Payment/order.html', context=context)
    except:
        messages.warning(request, 'You do not have an active order!')
        return redirect('App_Shop:home')


def apply_coupon(request):
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST, None)
        if coupon_form.is_valid():
            coupon_code = coupon_form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                order_qs = Order.objects.filter(user=request.user, ordered=False)
                order = order_qs[0]
                order.coupon = coupon
                order.save()
                return HttpResponseRedirect(reverse('App_Payment:checkout'))
            except ObjectDoesNotExist:
                messages.warning(request, 'Invalid coupon!')
                return HttpResponseRedirect(reverse('App_Payment:checkout'))

    else:
        raise ValueError('GET method not allowed')
