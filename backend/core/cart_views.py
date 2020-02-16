from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .models import Item, OrderItem, Order


@login_required
def add_to_cart(request, slug):
    """
    add to cart

    :param request:
    :param slug:
    """
    # get item, otherwise give 404 not found
    item = get_object_or_404(Item, slug=slug)
    # order the item
    order_item, created = OrderItem.objects.get_or_create(
        item=item, username_order_item=request.user, ordered=False)
    order_querySet = Order.objects.filter(
        username_order=request.user, ordered=False)

    if order_querySet.exists():
        order = order_querySet[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was update')
            return redirect('core:product', slug=slug)
        # otherwise add into cart
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('core:product', slug=slug)
    else:
        # set order date-time
        order_date = timezone.now()
        # create order
        order = Order.objects.create(
            username_order=request.user, order_date=order_date)
        order.items.add(order_item)
        # order added to cart [message]
        messages.info(request, 'This item was added to your cart')
        return redirect('core:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    """
    remove an item from cart

    :param request:
    :param slug:
    """
    # get item, otherwise give 404
    item = get_object_or_404(Item, slug=slug)
    # check if user had an order
    order_querySet = Order.objects.filter(
        username_order=request.user, ordered=False)
    # if user had an order
    if order_querySet.exists():
        # get|grab the order
        order = order_querySet[0]
        # check if the order item is in the order | slug
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, username_order_item=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.warning(request, 'This item was removed from your cart')
            return redirect('core:product', slug=slug)
        else:
            # return message [user doesn't contain the order item]
            messages.warning(request, 'This item was not in your cart')
            return redirect('core:product', slug=slug)
    else:
        # return message [user doesn't have an order]
        messages.warning(request, "You doesn't order this item")
        return redirect('core:product', slug=slug)


@login_required
def decrease_quantity(request, slug):
    """
    decrease the quantity of item

    :param request:
    :param slug:
    """
    # get item, otherwise give 404
    item = get_object_or_404(Item, slug=slug)
    # check if user had an order
    order_querySet = Order.objects.filter(
        username_order=request.user, ordered=False)
    # if user had an order
    if order_querySet.exists():
        # get|grab the order
        order = order_querySet[0]
        # check if the order item is in the order | slug
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, username_order_item=request.user, ordered=False)[0]
            order_item.quantity -= 1
            order_item.save()
            messages.warning(request, 'This item quantity was updated')
            return redirect('core:order-summary')

    return False


@login_required
def increase_quantity(request, slug):
    """
    increase the quantity of item

    :param request:
    :param slug:
    """
    # get item, otherwise give 404 not found
    item = get_object_or_404(Item, slug=slug)
    # order the item
    order_item, created = OrderItem.objects.get_or_create(
        item=item, username_order_item=request.user, ordered=False)
    order_querySet = Order.objects.filter(
        username_order=request.user, ordered=False)

    if order_querySet.exists():
        order = order_querySet[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was update')
            return redirect('core:order-summary')
        # otherwise add into cart
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart')
            return redirect('core:order-summary')

    return False