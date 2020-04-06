from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

class UserFile(models.Model):
    name = models.CharField(max_length=255, default="Untitled file")
    directory = models.CharField(max_length=2000)
    file = models.FileField(max_length=2000, storage=fs)
    favorite = models.BooleanField(default=False)
    comment = models.TextField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(default=timezone.now,
                            verbose_name="Date de création")
    last_modification = models.DateTimeField(default=timezone.now,
                            verbose_name="Date de la dernière modification")
    size = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, upload_to):
        for field in self._meta.fields:
            if field.name == "file":
                field.upload_to = upload_to # Absolute path to dir
        super(UserFile, self).save()
