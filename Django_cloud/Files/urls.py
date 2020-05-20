from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.TreeView.as_view()),
    url(r'^tree/(?P<path>.*)$', views.TreeView.as_view(), name='files'),
    url(r'^download/(?P<path>.*)$', views.DownloadView.as_view(), name='download'),
    url(r'^create_dir/(?P<path>.*)$', views.FolderCreationView.as_view(), name='create_dir'),
    url(r'^del_file/(?P<path>.*)$', views.del_file, name='del_file'),
    url(r'^fav/(?P<path>.*)$', views.fav, name='fav'),
    url(r'^favorites/$', views.fav_list, name='fav_list'),
    url(r'^last_files/$', views.last_files, name='recent'),
    url(r'^mv/', views.mv, name='move'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
]
