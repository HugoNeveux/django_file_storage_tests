from django import forms
from .models import UserFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(
                attrs={
                    'class': 'dropzone__file',
                    'id': 'file',
                    'data-multiple-caption': '{count} files selected',
                    'multiple': True
                }
            ),
        }
