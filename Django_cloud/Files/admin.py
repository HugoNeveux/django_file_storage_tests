from django.contrib import admin
from .models import UserFile

admin.site.register(UserFile)
admin.site.site_header = "DuplessCloud Administration"
