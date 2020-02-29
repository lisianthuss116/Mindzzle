from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image


class Profile(models.Model):
    user_account_name = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        default='avatar.svg',
        upload_to='user_image')
    created_date = models.DateTimeField(auto_now_add=True)
    activation_key = models.CharField(max_length=100, blank=True)
    key_expires = models.TextField(
        default=datetime.now()+timedelta(days=1),
        editable=False,
        max_length=20)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_account_name.username} Profile'

    def get_absolute_url(self):
        return reverse("account:profile", kwargs={
            "username": self.user_account_name.username})
