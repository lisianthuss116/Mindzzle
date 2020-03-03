from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from defender import signals

from account.models import Profile
import time

"""
when user has been save then send this signals
then receive by the decorator @receiver => excecute 'create_profile'
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    after an objects have been save => [post_save] | the user.
    auto create user-profile after user register

    :param sender:
    :param instance => User:
    :param created:
    """
    if created:
        if User.objects.get(pk=instance.id):
            Profile.objects.create(user_account_name=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    save created user-profile

    :param sender:
    :param instance => User:
    """
    instance.profile.save()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance, **kwargs):
    Token.objects.get_or_create(user=instance)

@receiver(signals.username_block)
def username_blocked(username, **kwargs):
    print("%s was blocked!" % username)

@receiver(signals.ip_block)
def ip_blocked(ip_address, **kwargs):
    print("%s was blocked!" % ip_address)

