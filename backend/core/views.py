from django.shortcuts import render
from .models import Item


def item_list(request):
    '''
    showing all item list

    :param request
    :return: render item-list
    '''
    context = {
        'items' : Item.objects.all()
    }

    return render(request, 'core/item_list.html', context)
