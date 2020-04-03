from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from django.urls import reverse

urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        authentication_form=CustomLoginForm
    ), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
]
