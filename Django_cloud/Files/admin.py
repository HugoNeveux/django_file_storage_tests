from django.contrib import admin
from .models import FavoriteFile, RecentFile

admin.site.register(FavoriteFile)
admin.site.register(RecentFile)
admin.site.site_header = "DuplessCloud Administration"
