from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^files/(?P<path>.*)$', views.files, name='files'),
    url(r'download/(?P<path>.*)$', views.download, name='download'),
    url(r'^create_dir/(?P<path>.*)$', views.folder_creation, name='create_dir'),
    url(r'^del_file/(?P<path>.*)$', views.del_file, name='del_file'),
    url(r'^fav/(?P<path>.*)$', views.fav, name='fav'),
    url(r'^favorites/$', views.fav_list, name='fav_list'),
    url(r'^last_files/$', views.last_files, name='recent')
]
