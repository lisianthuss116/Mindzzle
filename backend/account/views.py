from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from account.forms import UserRegistrationForm, UserLoginForm
from .models import Profile
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
# from api.serializers import LoginSerializer
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.contrib import messages
from account.services import *


def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True
            user_id = profile.user.id
        else:
            profile.user.is_active = True
            profile.user.save()
    else:
        already_active = True

    return render(request, 'account/activation.html', locals())


@require_http_methods(['GET', 'POST'])
def register(request):
    """
    user register new account

    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        # validate form
        if form.is_valid():
            datas = {}
            datas['email'] = form.cleaned_data['email']
            datas['username'] = form.cleaned_data['username']
            datas['password1'] = form.cleaned_data['password1']

            username_salt = datas['username']
            username_salt = username_salt.encode('utf-8')
            datas['activation_key'] = activation_code(username_salt)

            form.save(datas)
            # message [success]
            messages.success(request, 'Your account has been created!')
            # Redirect to login-page
            return redirect('login')
    # no requested data
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login(request):
    """
    user login

    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        # validate form
        if form.is_valid():
            # if data does valid, get fields
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                email=email, username=username, password=password)
            login_auth(request, user)
            # message [success]
            messages.success(request, 'Success login')
            # Redirect to login-page
            return redirect('/')
    # no requested data
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': Profile.objects.get(user_account_name=request.user.id),
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile_page/profile.html', context)
