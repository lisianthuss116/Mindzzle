from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .models import Item, OrderItem, Order


class Home(ListView):
    """
    showing all products

    :return render all products
    """
    # models
    model = Item
    # set pagianation
    paginate_by = 20
    # template directory
    template_name = 'core/home-page.html'


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
            return render(self.request, 'core/order_summary.html',context)

        except ObjectDoesNotExist:
            return render(self.request, 'core/order_summary.html')


class ProductDetail(DetailView):
    """
    showing specific product item

    :return all products
    """
    model = Item
    template_name = 'core/product.html'


@login_required
def checkout(request):
    """
    checkout

    :param request:
    """
    return render(request, 'core/checkout.html', context)


