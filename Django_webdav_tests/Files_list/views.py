from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

def upload_file(request):
    my_storage = FileSystemStorage()
    save = False
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        my_storage.save(request.FILES['file'].name,
            form.cleaned_data['file'])
        save = True
    return render(request, 'upload.html', {
        'form': form,
        'save': save,
        'content_files': my_storage.listdir(my_storage.base_url)[1]
    })
