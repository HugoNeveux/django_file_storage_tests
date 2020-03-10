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
from django.shortcuts import get_object_or_404


@login_required
def files(request, path=""):
    """Main view
    * File reception (javascript upload)
    * File list (showing uploaded files / folder navigation)"""
    # Variables and file storage initialisation
    current_dir = os.path.join(f"{request.user.username}", "files", path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, current_dir)
    files = []
    directories = []
    print(absolute_path)
    fs = FileSystemStorage(absolute_path)

    logged_user = User.objects.get(username=request.user.username, id=request.user.id)
    # dir_obj = get_object_or_404(UserDirectory, directory=path, owner=logged_user.id)

    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        file = UserFile(file = request.FILES['file'],
                        name = request.FILES['file'].name,
                        owner = request.user,
                        directory=UserDirectory.objects.filter(directory=path)[0])
        file.save(os.path.join(settings.MEDIA_ROOT, current_dir))

    # Showing directory content

    directories_names = fs.listdir(".")[0]
    files_names = fs.listdir(".")[1]
    for name in files_names:
        files = UserFile.objects.filter(file=os.path.join(path, name),
                                        owner=request.user.id)
    for name in directories_names:
        directories += UserDirectory.objects.filter(directory=f"{path}{name}/",
                                                    owner=request.user.id)


    print(files, directories)

    for element in files:    # Listing files
        files.append(element)
    # Showing web page & rendering template
    return render(request, 'upload.html', {
        'form': form,
        'directory_files': files,
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
    if not UserDirectory.objects.filter(directory=folder_path).count():
        dir = UserDirectory(directory=folder_path, owner=request.user, name=path.split("/")[-1])
        os.mkdir(folder_path)
        dir.save(folder_path)
    return redirect(f"/files/{path}")
