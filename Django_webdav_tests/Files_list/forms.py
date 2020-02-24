from django import forms
from .models import UserFile
from django.contrib.auth.forms import AuthenticationForm

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'dropzone__file',
            'id': 'file', 'multiple': 1, 'data-multiple-caption': '{count} files selected'})

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe'}))
