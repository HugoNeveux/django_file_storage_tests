from django.forms import ModelForm, TextInput, EmailInput, Select
from Auth.models import Profile
from django.contrib.auth.models import User
from Auth.choices import THEME_CHOICES
from django.contrib.auth.forms import UserChangeForm

class UserForm(ModelForm):
    """
    Main settings form for user object
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': TextInput(
                attrs = {
                    'class': 'form-control mb-3',
                    'label': 'Nom d\'utilisateur'
                }
            ),
            'first_name': TextInput(
                attrs = {
                    'class': 'form-control mb-3',
                }
            ),
            'last_name': TextInput(
                attrs = {
                    'class': 'form-control mb-3',
                }
            ),
            'email': EmailInput(
                attrs = {
                    'class': 'form-control mb-3',
                }
            )
        }
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom de famille",
            'email': "Adresse mail",
        }

class ProfileForm(ModelForm):
    """
    Secondary settings form, for user profile
    """
    class Meta:
        model = Profile
        fields = ['theme']
        widgets = {
            'theme': Select(
                attrs = {
                    'class': 'form-control',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['theme'].required = False
