from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.conf import settings
from .choices import THEME_CHOICES
import os
import shutil


class Profile(models.Model):
    """
    Extension of user model, which contains extra informations (spaced used,
    max space available and user theme)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upload_limit = models.BigIntegerField(default=1073741824)
    total_used = models.BigIntegerField(default=0)
    theme = models.IntegerField(choices=THEME_CHOICES, default=1)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)


@receiver(pre_save, sender=User)
def create_user_files(sender, instance, **kwargs):
    """
    Creates user files in /media/ if user was just created or renames it if
    user changes his username
    """
    if User.objects.filter(username=instance.username).count() == 0 and User.objects.filter(id=instance.id).count() > 0:
        os.rename(os.path.join(settings.MEDIA_ROOT, User.objects.get(id=instance.id).username),
                  os.path.join(settings.MEDIA_ROOT, instance.username))
    elif User.objects.filter(username=instance.username, id=instance.id).count() == 0:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, instance.username))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, instance.username, "files"))


@receiver(post_save, sender=User)
def link_to_profile(sender, instance, **kwargs):
    """
    Creates user profile when a new user is created
    """
    if Profile.objects.filter(user=instance).count() == 0:
        profil = Profile(user=instance)
        profil.save()


@receiver(post_delete, sender=User)
def delete_user_files(sender, instance, **kwargs):
    """
    Removes user files when user is deleted
    """
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, instance.username))
