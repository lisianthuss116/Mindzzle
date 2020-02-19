from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user_account_name = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        default='avatar.svg',
        upload_to='user_image')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_account_name.username} Profile'
