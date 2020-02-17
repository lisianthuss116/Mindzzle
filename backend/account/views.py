from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import UserRegistrationForm
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET','POST'])
def register(request):
    """
    user register new account

    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        # validate form
        if form.is_valid():
            form.save()
            # if data does not valid, return only username field
            username = form.cleaned_data.get('username')
            # message [success]
            messages.success(request, 'Your account has been created!')
            # Redirect to login-page
            return redirect('login')

    # no requested data
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'auth/register.html', context)
