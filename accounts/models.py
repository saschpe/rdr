# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models


class UserProfile(models.Model):
    '''Additional user information.

    See https://docs.djangoproject.com/en/1.3/topics/auth/#storing-additional-information-about-users
    '''
    image = models.ImageField()
    user = models.OneToOneField(User)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
