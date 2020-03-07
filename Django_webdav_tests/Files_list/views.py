import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomLoginForm
from .models import UserFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import unquote


@login_required
def files(request, path=""):
    """Main view
    * File reception (javascript upload)
    * File list (showing uploaded files / folder navigation)"""
    # Variables and file storage initialisation
    root = settings.MEDIA_ROOT
    current_directory = root + f"/{request.user.username}/files/" + path
    directory_files = []
    directory_directories = []
    files_storage = FileSystemStorage(location=current_directory, base_url=current_directory)
    storage = UserFile()

    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        storage.file = request.FILES['file']
        storage.storage_dir = path
        storage.save(current_directory)
    print(request.FILES)

    # Showing directory content
    files_and_folders = files_storage.listdir(current_directory)
    for element in files_and_folders[1]:    # Listing files
        directory_files.append({"file": element, "url": path + element + "/"})
    for element in files_and_folders[0]:    # Listing folders
        directory_directories.append({"directory": element, "url": path + element + "/"})
    # Showing web page & rendering template
    return render(request, 'upload.html', {
        'form': form,
        'directory_files': directory_files,
        'directory_directories': directory_directories,
    })

@login_required()
def download(request, path):
    """Download file when clicking on it"""
    file_path = os.path.join(settings.MEDIA_ROOT, request.user.username, "files", path)
    file_path = unquote(file_path)
    if file_path.endswith("/"):
        file_path = file_path[0:-1]
    if os.path.exists(file_path):
        try:
            return FileResponse(open(file_path, 'rb') , os.path.basename(file_path), as_attachment=True)
        except IsADirectoryError:
            return redirect("/files/")
    raise Http404

def logout_login(request):
    """Logout user, then show login page"""
    return auth_views.logout_then_login(request, login_url=reverse("login"))

@login_required
def folder_creation(request, path):
    """Folder creation"""
    folder_path = os.path.join(settings.MEDIA_ROOT, request.user.username, "files", path)
    folder_path = unquote(folder_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return redirect(f"/files/{path}")
