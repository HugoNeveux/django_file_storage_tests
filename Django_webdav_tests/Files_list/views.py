from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.utils.datastructures import MultiValueDictKeyError

def files(request, path=""):
    files_storage = FileSystemStorage(base_url = settings.MEDIA_ROOT)
    root = settings.MEDIA_ROOT
    current_directory = root + "/" + path
    directory_files = []
    directory_directories = []
    # Upload
    # form = UploadFileForm(request.POST or None, request.FILES)
    # if form.is_valid():
    #     files_storage.save(request.FILES['file'].name,
    #         form.cleaned_data['file'])
    print(request.FILES)
    try:
        print(request.FILES['files[]'])
    except MultiValueDictKeyError:
        print("AUCUN FICHIER ENVOYE")

    # Showing directory content
    files_and_folders = files_storage.listdir(current_directory)
    print(files_and_folders)
    for element in files_and_folders[1]:
        directory_files.append({"file": element, "url": files_storage.path(element) + "/"})
    for element in files_and_folders[0]:
        directory_directories.append({"directory": element, "url":  files_storage.path(element) + "/"})
    return render(request, 'upload.html', {
        # 'form': form,
        'directory_files': directory_files,
        'directory_directories': directory_directories,
    })


# def files(request, path=""):
#     root = settings.MEDIA_ROOT
#     files_storage = FileSystemStorage(base_url = root)
#
#     # File upload
#     uploaded_files = request.FILES
#     print(uploaded_files)
#     return render(request, 'upload.html', {
#         'directory_files': None,
#         'directory_directories': None,
#     })



def download(request, path):
    """Allows to download file"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if file_path.endswith("/"):
        file_path = file_path[0:-1]
        print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb') , os.path.basename(file_path))
    raise Http404
