from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    # user       = models.OneToOneField(User, on_delete=models.CASCADE)
    user       = models.CharField(default='Anonymous', max_length=60)
    user_image = models.ImageField(
        default = 'avatar.svg',
        upload_to= 'UserImages'

    )
    def __str__(self):
        return f'{self.user} Profile'
