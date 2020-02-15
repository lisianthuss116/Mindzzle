from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.utils import timezone


class Home(ListView):
    '''
    showing all item list

    :return: render item-list
    '''
    model = Item
    template_name = 'core/home-page.html'


class ProductDetail(DetailView):
    '''
    showing specific product item

    :return: all products
    '''
    model = Item
    template_name = 'core/product.html'


def checkout(request):
    '''
    checkout

    :param request
    '''
    return render(request, 'core/checkout.html', context)


def add_to_cart(request, slug):
    '''
    add to cart

    :param request
    :param slug
    '''
    # get item, otherwise give 404 not found
    item = get_object_or_404(Item, slug=slug)
    # order the item
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_querySet = Order.objects.filter(user=request.user, ordered=False)

    if order_querySet.exists():
        order = order_querySet[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was update')
            return redirect('core:product', slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('core:product', slug=slug)
    else:
        # set order date-time
        order_date = timezone.now()
        # create order
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(order_item)
        # order added to cart [message]
        messages.info(request, 'This item was added to your cart')
        return redirect('core:product', slug=slug)


def remove_from_cart(request, slug):
    '''
    remove an item from cart

    :param request
    :param slug
    '''
    # get item, otherwise give 404
    item = get_object_or_404(Item, slug=slug)
    # check if user had an order
    order_querySet = Order.objects.filter(user=request.user, ordered=False)
    # if user had an order
    if order_querySet.exists():
        # get|grab the order
        order = order_querySet[0]
        # check if the order item is in the order | slug
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, 'This item was removed from your cart')
            return redirect('core:product', slug=slug)
        else :
            # return message [user doesn't contain the order item]
            messages.info(request, 'This item was not in your cart')
            return redirect('core:product', slug=slug)
    else:
        # return message [user doesn't have an order]
        messages.info(request, "You doesn't order this item")
        return redirect('core:product', slug=slug)
