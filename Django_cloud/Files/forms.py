from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'dropzone__file',
        'id': 'file',
        'data-multiple-caption': '{count} files selected',
        'multiple': True
        }
    ))
