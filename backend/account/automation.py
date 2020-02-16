from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

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
        Profile.objects.create(user_account_name=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    save created user-profile

    :param sender:
    :param instance => User:
    """
    instance.profile.save()
