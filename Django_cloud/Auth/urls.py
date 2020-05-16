from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm, CustomPasswordChangeForm
from django.urls import reverse

urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        authentication_form=CustomLoginForm
    ), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^change_password/$', auth_views.PasswordChangeView.as_view(
        template_name='custom_registration/password_change_form.html',
        form_class=CustomPasswordChangeForm), name="change_password"),
    url(r'^change_password_done/$',
        auth_views.PasswordChangeDoneView.as_view(
        template_name='custom_registration/password_change_done.html'),
        name="password_change_done"),
]
