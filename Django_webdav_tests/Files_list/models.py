from django.db import models

class UserFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()

    def __str__(self):
        return self.name
