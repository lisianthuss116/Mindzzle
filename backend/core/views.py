from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.core.cache import cache
from django.conf import settings
from api.serializers import AllItemSerializer
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import json

from core.forms import CheckoutForm
import requests
from core.models import (
    Item,
    OrderItem,
    Order,
    BillingAddress)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def home_view(request):
    paginate_by = 25
    template = 'core/home-page.html'

    if request.method == "GET":
        if 'item_list' in cache:
            item_list = cache.get('item_list')
            item_list = json.loads(item_list)
        else:
            item_list = serializers.serialize('json', Item.objects.all())
            cache.set('item_list', item_list, timeout=CACHE_TTL)
            item_list = json.loads(item_list)

        paginator = Paginator(item_list, paginate_by)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        context = {
            'items': products
        }

        if type(item_list) is str or isinstance(item_list, str):
            return JsonResponse(
                {'failed': 'THE DATA IS NOT A LIST OR JSON. DATA:[{}]'.format(type(item_list))})
        else:
            return render(request, template, context)


class Home(ListView):
    """
    showing all products

    :return render all products
    """
    model = Item.objects.all()
    paginate_by = 25
    template_name = 'core/home-page.html'

    def get(self, request):
        paginator = Paginator(self.model.order_by(
            'created_date'), self.paginate_by)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        # context data
        context = {
            'items': products}

        return render(request, self.template_name, context)


class OrderSummary(LoginRequiredMixin, View):
    """
    showing all products in user cart

    :return render all products
    """

    def get(self, *args, **kwargs):
        try:
            ordered_product = Order.objects.get(
                username_order=self.request.user, ordered=False)
            context = {
                'ordered_products': ordered_product
            }

            return render(self.request, 'core/order_summary.html', context)

        except ObjectDoesNotExist:
            return render(self.request, 'core/order_summary.html')


class ProductDetail(DetailView):
    """
    showing specific product item

    :return all products
    """
    model = Item
    template_name = 'core/product.html'


class CheckoutView(View):
    def get(self, *args, **kwargs):

        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'core/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            ordered_product = Order.objects.get(
                username_order=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                billing_zip = form.cleaned_data.get('billing_zip')

                # TODO:Add Function for These Fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')

                payment_options = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    username_order=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    billing_zip=billing_zip)
                billing_address.save()
                ordered_product.billing_address = billing_address
                ordered_product.save()
                # TODO Added redirect to the selected payment option
                return redirect('core:checkout')
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You not order yet!")
            return redirect('order_summary.html')
