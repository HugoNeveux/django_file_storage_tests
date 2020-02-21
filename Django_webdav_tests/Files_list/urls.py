from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^files/(?P<path>.*)$', views.files, name='files'),
    url(r'download/(?P<path>.*)$', views.download, name='download'),
    url(r'^$', auth_views.LoginView.as_view())
]
