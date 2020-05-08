from django.db import models
from Files.models import UserFile
from django.contrib.auth.models import User
import random, string

class ShareLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    to_file = models.ForeignKey(to=UserFile, on_delete=models.CASCADE)

    def link_generation():
        chars = string.ascii_letters + string.digits
        rand = [random.choice(chars) for _ in range(16)]
        code = ''.join(rand)
        if ShareLink.objects.filter(link=code).exists():
            return self.link_generation(nb_chars)
        return code
