from django.db import models

class UserFile(models.Model):
    file = models.FileField()

    def __str__(self):
        return self.name
