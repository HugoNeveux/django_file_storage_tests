from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


urlpatterns = [
    url(r'^$', views.FileUploadAndListView.as_view()),
    url(r'^tree/(?P<path>.*)$', views.FileUploadAndListView.as_view(), name='files'),
    url(r'^download_dir/(?P<path>.*)$', views.download_dir, name='download_dir'),
    url(r'download_file/(?P<id>\d+)/', views.download_file, name='download_file'),
    url(r'^create_dir/(?P<path>.*)$', views.folder_creation, name='create_dir'),
    url(r'^del_file/(?P<path>.*)$', views.del_file, name='del_file'),
    url(r'^fav/(?P<path>.*)$', views.fav, name='fav'),
    url(r'^favorites/$', views.fav_list, name='fav_list'),
    url(r'^last_files/$', views.last_files, name='recent'),
    url(r'^mv/', views.mv, name='move')
]
