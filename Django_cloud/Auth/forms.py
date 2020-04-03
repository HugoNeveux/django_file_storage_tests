from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe'}))
