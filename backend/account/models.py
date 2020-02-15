from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.CharField(default='Anonymous', max_length=69)
    user_image = models.ImageField(
        default='avatar.svg',
        upload_to='user_image')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} Profile'
