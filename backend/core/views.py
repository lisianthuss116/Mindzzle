from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

class Home(ListView) :
    '''
    showing all item list

    :param request
    :return: render item-list
    '''
    model = Item
    template_name = 'core/home-page.html'

class ProductDetail(DetailView) :
    '''
    showing specific product item

    :param request
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
