from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse

def files(request, path=""):
    files_storage = FileSystemStorage(base_url = settings.MEDIA_ROOT)
    directory_files = []
    directory_directories = []
    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        files_storage.save(request.FILES['file'].name,
            form.cleaned_data['file'])

    # Showing directory content
    files_and_folders = files_storage.listdir(files_storage.base_url + path)
    print(files_and_folders)
    for element in files_and_folders[1]:
        directory_files.append({"file": element, "url": path + files_storage.url(element)  + "/"})
    for element in files_and_folders[0]:
        directory_directories.append({"directory": element, "url": path + files_storage.url(element) + "/"})
    return render(request, 'upload.html', {
        'form': form,
        'directory_files': directory_files,
        'directory_directories': directory_directories,
    })

def download(request, path):
    """Allows to download file"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if file_path.endswith("/"):
        file_path = file_path[0:-1]
        print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb') , os.path.basename(file_path))
    raise Http404
