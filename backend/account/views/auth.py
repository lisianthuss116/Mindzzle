from django.views.decorators.http import require_http_methods
from django.views import View
from django.template.loader import get_template
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import admin, messages
from django.contrib.auth import authenticate, login as login_auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.mail.backends.smtp import EmailBackend

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from account.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm)
from account.models import Profile
from account.services.tokens import user_tokenizer
from account.services.email import email
from account.services import activation_key, generate


class RegisterView(View):
    """
    user register new account

    :param request:
    :method POST | GET:
    :return render register page
    """

    def get(self, request):
        """
        user register form

        :param request:
        """
        # render register page [if user is not give any post request]
        return render(request, 'auth/register.html',
                      {'form': UserRegistrationForm()})

    def post(self, request):
        """
        user register form [post data user]

        :param request:
        """
        # get requested post form
        form = UserRegistrationForm(request.POST or None)
        # validate form
        if form.is_valid():
            # set datas variables
            datas = {}
            datas['email'] = form.cleaned_data['email']
            datas['username'] = form.cleaned_data['username']
            datas['password1'] = form.cleaned_data['password1']
            # set username salt
            username_salt = datas['username'].encode('utf-8')
            # save user [account not verificated yet] bring some datas
            user = form.save(datas)
            user.is_valid = False
            user.save()

            # generate token
            token = user_tokenizer.make_token(user)
            # generate unique user-id
            user_id = generate.set_user_id(user.id)
            # create url activation
            url = 'http://127.0.0.1:8000' + reverse('confirm-email',
                                                    kwargs={'user_id': user_id, 'token': token})
            message = url
            # email to user-email [new-user-account]
            email(request, user.email, message)

            # render login page after register, and give some message that user-account is not verificated yet
            messages.warning(request, f'A confirmation email has been sent to {user.email}')
            return redirect('auth:login')
        # register-form is not valid, return to register page
        return render(request, 'auth/register.html',
                      {'form': UserRegistrationForm()})


class ConfirmRegisterView(View):
    def get(self, request, user_id, token):
        """
        user success confirmation activation page

        :param request:
        :param user_id:
        :param token:
        """
        # get user id
        user_id = generate.get_real_user_id(user_id)
        # check if user has been registered and not activated
        if get_object_or_404(User.objects.all(), pk=user_id):
            # get user and user-profile
            user = User.objects.get(pk=user_id)
            user_profile = Profile.objects.get(user_account_name=user_id)
            # [failed] message
            context = {
                'form': AuthenticationForm(),
                'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'}

            # check user and user token
            if user and user_tokenizer.check_token(user, token):
                # user had been activated
                user.is_valid = True
                # user-profile had been activated
                user_profile.is_valid = True
                user_profile.activation_key = activation_key.activation_code(
                    user_id)

                # save new user [user has been activated]
                user.save()
                user_profile.save()
                # [success] message
                context['message'] = 'Registration complete, Please login.'

            # render activation page
            return render(request, 'account/activation.html', context)


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

        username = request.POST.get("username")
        user = User.objects.get(username=username)
        activated = Profile.objects.get(user_account_name=user.id)

        if activated.activation_key and activated.is_valid == True:
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

        messages.error(request, 'Your account is not activated yet, please activate your account. check you email inbox, or your spam email !')
        return redirect('auth:login')
    # no requested data
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)
