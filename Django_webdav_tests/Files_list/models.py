from django.db import models

class UserFile(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
