from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

class FavoriteFiles(models.Model):
    path = models.CharField(max_length=2000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RecentFiles(models.Model):
    path = models.CharField(max_length=2000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modification = models.DateTimeField(default=timezone.now,
                            verbose_name="Date de la dernière modification")

    def __str__(self):
        return self.name
