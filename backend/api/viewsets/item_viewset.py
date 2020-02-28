from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser

from api.serializers import ItemSerializer, AllItemSerializer
from core.models import Item


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
@cache_page(CACHE_TTL)
def item_view(request):
    """
    show all item

    :param request:
    :method GET | POST:
    :return Json-response:
    """

    if request.method == "GET":
        # check if data is exists in cache
        if 'item_list' in cache:
            # get cached data
            item_list = cache.get('item_list')
            # give the cached data
            return JsonResponse(item_list, safe=False)

        else:
            # create cache data
            data = serializers.serialize(
                'json', Item.objects.all().order_by('id'))
            # set cache
            cache.set('item_list', data, timeout=CACHE_TTL)

            # show the current [not in cache]
            queryset = Item.objects.all().order_by('id')
            serializer = AllItemSerializer(queryset, many=True)
            # safe=False [cuz the data is not an a dict-type]
            return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        # instanciate json-parser
        json_parser = JSONParser()
        # parse data
        data = json_parser.parse(request)
        # serialize
        serializer = AllItemSerializer(data=data)
        # check serializer
        if serializer.is_valid():
            # save
            serializer.save()
            # return success 201
            return JsonResponse(serializer.data, status=201)
        # return bad-request 400
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    """
    show all item

    :param request:
    :method PUT | DELETE:
    :return Json-response:
    """
    try:
        instance = get_object_or_404(Item.objects.all(), pk=pk)
    except Item.DoesNotExists as not_exist:
        return JsonResponse({"error": "Given item not found"}, status=400)

    if request.method == "GET":
        serializer = AllItemSerializer(instance)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = AllItemSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        instance.delete()
        return JsonResponse(
            {"success": "Propper item successfull deleted"}, status=204)
