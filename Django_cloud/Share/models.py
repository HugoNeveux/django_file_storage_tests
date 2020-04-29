from django.db import models
from Files.models import UserFile
from django.contrib.auth.models import User
import random, string

class ShareLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    to_file = models.ForeignKey(to=UserFile, on_delete=models.CASCADE)

    def link_generation(nb_chars):
        chars = string.ascii_letters + string.digits
        random = [random.choice(chars) for _ in range(nb_chars)]
        code = ''.join(random)
        if ShareLink.objects.filter(url=code).exists():
            return self.link_generation(nb_chars)
        return code
