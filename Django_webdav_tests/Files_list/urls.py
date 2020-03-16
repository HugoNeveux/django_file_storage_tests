from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

urlpatterns = [
    url(r'^files/(?P<path>.*)$', views.files, name='files'),
    url(r'download/(?P<path>.*)$', views.download, name='download'),
    url(r'^$', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        authentication_form=CustomLoginForm
        ), name='login'),
    url(r'^logout/$', views.logout_login, name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^create_dir/(?P<path>.*)$', views.folder_creation, name='create_dir'),
    url(r'^del_file/(?P<path>.*)$', views.del_file, name='del_file'),
]
