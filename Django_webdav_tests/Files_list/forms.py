from django import forms
from .models import UserFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'dropzone__file',
            'id': 'file', 'multiple': 1, 'data-multiple-caption': '{count} files selected'})
