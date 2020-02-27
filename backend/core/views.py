from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.forms import CheckoutForm
import requests
from core.models import (
    Item,
    OrderItem,
    Order,
    BillingAddress)


class Home(ListView):
    """
    showing all products

    :return render all products
    """
    model = Item.objects.all()
    paginate_by = 25
    template_name = 'core/home-page.html'

    @method_decorator(login_required)
    def get(self, request):
        item_from_api = requests.get('http://127.0.0.1:8000/api/v2/items/')
        json = item_from_api.json()

        paginator = Paginator(self.model.order_by(
            'created_date'), self.paginate_by)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        context = {'items': products, 'json_data':json}

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
                    billing_zip=billing_zip
                )
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
