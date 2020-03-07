from django.db import models
import os


class UserFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(max_length=5000)
    favorite = models.BooleanField(default=False)
    comment = models.TextField(max_length=255)
    storage_dir = models.URLField(max_length=5000)

    def __str__(self):
        return self.name

    def save(self, upload_to):
        for field in self._meta.fields:
            if field.name == "file":
                field.upload_to = upload_to
        super(UserFile, self).save()
