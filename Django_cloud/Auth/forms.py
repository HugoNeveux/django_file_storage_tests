from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with placeholders for user login page
    """
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe'}))

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with changed fields size for user settings
    """
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-100 mb-3'
