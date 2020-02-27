from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Item

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'price',
            'description_item',
            'discount_price',
            'category',
            'label',
            'slug',
        ]

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get("username", "")
#         password = data.get("password", "")

#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     data["user"] = user
#                 else:
#                     msg = "User is deactivated"
#                     raise Exception(msg)
#             else:
#                 msg = "Unable to login with given credentials"
#                 raise Exception(msg)
#         else:
#             msg = "Must Provide Username And Password Both"
#             raise Exception(msg)
#         return data