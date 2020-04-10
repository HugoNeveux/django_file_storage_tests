from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.main, name="settings_main"),
    url(r'^change_password/$', auth_views.PasswordChangeView.as_view(), name="change_password"),
]
