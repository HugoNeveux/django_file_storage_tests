from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os


fs = FileSystemStorage()

class UserFile(models.Model):
    name = models.CharField(max_length=255, default="Untitled file")
    directory = models.CharField(max_length=2000)
    file = models.FileField(max_length=2000, storage=fs)    # RELATIVE path to file
    favorite = models.BooleanField(default=False)
    comment = models.TextField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(default=timezone.now,
                            verbose_name="Date de création")

    def __str__(self):
        return self.name

    def save(self, upload_to):
        for field in self._meta.fields:
            if field.name == "file":
                field.upload_to = upload_to
        super(UserFile, self).save()

@receiver(pre_save, sender=User)
def create_user_files(sender, instance, **kwargs):
    if User.objects.filter(username=instance.username).count() == 0:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, instance.username))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, instance.username, "files"))
