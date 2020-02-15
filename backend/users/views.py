from django.contrib import admin
from django.shortcuts import render
from .models import Profile


def profile(request) :
    context = {
        'users': Profile.objects.all()
    }
    return render(request, 'users/index.html', context)