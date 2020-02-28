from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from account.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm)
from account.models import Profile


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
