import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomLoginForm
from .models import UserFile, UserDirectory
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import unquote


@login_required
def files(request, path=""):
    """Main view
    * File reception (javascript upload)
    * File list (showing uploaded files / folder navigation)"""
    # Variables and file storage initialisation
    ROOT = settings.MEDIA_ROOT
    current_dir = f"{request.user.username}/files/" + path
    directory_files = []
    print(current_dir)

    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        file = UserFile(file = request.FILES['file'],
                        name = request.FILES['file'].name,
                        owner = request.user,
                        directory=UserDirectory.objects.filter(directory=current_dir)[0])
        file.save(ROOT + "/" + current_dir)
        print(ROOT + "/" + current_dir)

    # Showing directory content
    files = UserFile.objects.filter(directory=UserDirectory.objects.filter(directory=current_dir)[0])
    directories_names = [ name for name in os.listdir(f"{ROOT}/{current_dir}") if os.path.isdir(os.path.join(f"{ROOT}/{current_dir}", name)) ]
    print(directories_names)
    directories = []
    for name in directories_names:
        directories += UserDirectory.objects.filter(directory=os.path.join(current_dir, name))
    for element in files:    # Listing files
        directory_files.append(element)
    # Showing web page & rendering template
    return render(request, 'upload.html', {
        'form': form,
        'directory_files': directory_files,
        'directory_directories': directories,
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
    folder_path = os.path.join(request.user.username, "files", path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, folder_path)
    if not UserDirectory.objects.filter(directory=folder_path).count():
        dir = UserDirectory(directory=folder_path, owner=request.user, name=path.split("/")[-1])
        os.mkdir(absolute_path)
        dir.save(absolute_path)
    return redirect(f"/files/{path}")
