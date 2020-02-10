from django.shortcuts import render
from .forms import UploadFileForm
from .models import UserFile

def upload_file(request):
    save = False
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        f = UserFile()
        f.name = form.cleaned_data['name']
        f.file = form.cleaned_data['file']
        f.save()
        save = True

    return render(request, 'upload.html', {
        'form': form,
        'sauvegarde': save
    })
