from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^files/(?P<path>.*)$', views.files, name='files'),
    url(r'download/(?P<path>.*)$', views.download, name='download')
]
