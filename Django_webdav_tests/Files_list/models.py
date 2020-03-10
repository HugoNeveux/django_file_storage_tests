from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import os


class UserDirectory(models.Model):
    directory = models.FileField(max_length=255)    # RELATIVE path to directory
    name = models.CharField(max_length=255, default="Folder")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, upload_to):
        for field in self._meta.fields:
            if field.name == "directory":
                field.upload_to = os.path.join(settings.MEDIA_ROOT, upload_to)
        super(UserDirectory, self).save()


class UserFile(models.Model):
    name = models.CharField(max_length=255, default="Untitled file")
    file = models.FileField(max_length=5000)    # RELATIVE path to file
    favorite = models.BooleanField(default=False)
    comment = models.TextField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(default=timezone.now,
                            verbose_name="Date de création")
    directory = models.ForeignKey(UserDirectory, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def save(self, upload_to):
        for field in self._meta.fields:
            if field.name == "file":
                field.upload_to = os.path.join(settings.MEDIA_ROOT, upload_to)
        super(UserFile, self).save()
