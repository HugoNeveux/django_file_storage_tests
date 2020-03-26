import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomLoginForm
from .models import UserFile
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import unquote
from django.shortcuts import get_object_or_404
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import shutil

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

    logged_user = User.objects.get(username=request.user.username, id=request.user.id)

    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)
    if form.is_valid():
        existing_file = UserFile.objects.filter(directory=absolute_path, owner=request.user.id, name=request.FILES['file'].name)
        if existing_file.count():
            existing_file[0].file = request.FILES["file"]
            existing_file[0].save(current_dir)
        else:
            file = UserFile(file = request.FILES["file"],
            name = request.FILES["file"].name,
            owner = request.user,
            directory=absolute_path)
            file.save(os.path.join(settings.MEDIA_ROOT, current_dir))

    # Showing directory content
    files = UserFile.objects.filter(directory=absolute_path, owner=request.user.id)
    # files_to_json = UserFile.objects.filter(directory=absolute_path, owner=request.user.id).values_list('name')
    # files_json = json.dumps(list(files), cls=DjangoJSONEncoder)
    tmp_json = serializers.serialize("json", files)
    files_json = json.dumps(json.loads(tmp_json))
    directories_names = [ dir for dir in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, dir))]
    print(directories_names)
    for name in directories_names:
        directories.append({'name': name, 'url': os.path.join(path, name)})

    breadcrumb = {}
    full_path = path.replace("/", "\\").split("\\")
    breadcrumb["path"] = []
    to_dir = ""
    for dir in full_path[:-1]:
        to_dir = os.path.join(to_dir, dir)
        breadcrumb["path"].append([dir, to_dir])

    breadcrumb["active"] = full_path[-1]
    print(breadcrumb)
    # Showing web page & rendering template
    return render(request, 'files.html', {
        'form': form,
        'directory_files': files,
        'directory_directories': directories,
        'breadcrumb': breadcrumb,
        'files_json': files_json,
        'current_dir': path,
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
    name = request.GET.get('dirname')
    if name:
        folder_path = os.path.join(settings.MEDIA_ROOT, request.user.username, "files", path, name)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
    return redirect(f"/files/{path}")

@login_required
def del_file(request, path):
    """File or folder deletion"""
    redirection = request.GET.get('redirect')
    if os.path.isfile(path):
        file = UserFile.objects.filter(file=path, owner=request.user.id).delete()
        os.remove(path)
    else:
        path = os.path.join(settings.MEDIA_ROOT, request.user.username, "files", path)
        dir_contents = os.listdir(path)
        if len(dir_contents) == 0:
            os.rmdir(path)
        else:
            shutil.rmtree(path)

    return redirect(f"/files/{redirection}")

@login_required
def fav(request, path):
    filename = request.GET.get('filename')
    to_file = os.path.join(settings.MEDIA_ROOT, request.user.username, "files", path)
    print(to_file)
    file = UserFile.objects.get(file=os.path.join(to_file, filename), owner=request.user.id)
    if not file.favorite:
        file.favorite = True
    else:
        file.favorite = False
    file.save(to_file)
    return redirect(f"/files/{path}")

@login_required
def fav_list(request):
    files = UserFile.objects.filter(favorite=True, owner=request.user.id)
    return render(request, 'files.html', {
        'directory_files': files,
        'directory_directories': [],
    })
