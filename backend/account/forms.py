from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from account.models import Profile
import datetime

password_validate = """
<ul>
    <li>Your password can't be too similar to your other personal information.</li>
    <li>Your password must contain at least 8 characters.</li>
    <li>Your password can't be a commonly used password.</li>
    <li>Your password can't be entirely numeric.</li>
<ul>
"""


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Must be a valid email. And consider to using @gmail, or etc.',
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g : johndoe32@gmail.com',
            'autofocus': 'on'
        }))
    username = forms.CharField(
        max_length=50,
        help_text='Please consider when creating the username, because you will cannot change your username !',
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g : John Doe',
            'autofocus':'off'
        }))

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2'
        ]

    def save(self, datas):
        user = User.objects.create_user(
            datas['username'], datas['email'], datas['password1'])
        user.save()

        profile = Profile()
        profile.activation_key = datas['activation_key']
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        help_text='Must be a valid email. And consider to using @gmail, or etc.')
    username = forms.CharField(help_text='Must be a valid username')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if True:
            user = authenticate(
                email=email, username=username, password=password)
            if user:
                if not user:
                    raise forms.ValidationError("This user does not exists !")
            return super(UserLoginForm, self).clean(*args, **kwargs)

        return False


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        attrs = {'readonly': True}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_image']
