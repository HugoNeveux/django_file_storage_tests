import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UserFile
from Auth.models import Profile
from django.conf import settings
from django.http import Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from urllib.parse import unquote
from django.shortcuts import get_object_or_404
import json
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from .size import format_bytes
import shutil


@login_required
def tree(request, path=""):
    """Main view
    * File reception (javascript upload)
    * File list (showing uploaded files / folder navigation)"""
    # Variables and file storage initialisation
    current_dir = os.path.join(request.user.username, "files", path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, current_dir)
    files = []
    directories = []
    upload_error = False

    # Space available
    user_profile = Profile.objects.get(user=request.user.id)
    space = {"available": format_bytes(user_profile.upload_limit),
            "used": format_bytes(user_profile.total_used),
            "available_b": user_profile.upload_limit - user_profile.total_used }

    # Upload
    form = UploadFileForm(request.POST or None, request.FILES)

    if form.is_valid():
        existing_file = UserFile.objects.filter(
            directory=current_dir, owner=request.user.id, name=request.FILES['file'].name)
        if existing_file.count():
            old_size = existing_file[0].size
            new_size = existing_file[0].size + (old_size - form.cleaned_data["file"].size)
            existing_file[0].file = form.cleaned_data["file"]
            existing_file[0].size == new_size
            user_profile.total_used += old_size - form.cleaned_data["file"].size
            if user_profile.total_used <= user_profile.upload_limit:
                user_profile.save()
                existing_file[0].save(current_dir)
        else:
            file = UserFile(file=form.cleaned_data["file"],
                            name=form.cleaned_data["file"].name,
                            owner=request.user,
                            directory=current_dir,
                            size=form.cleaned_data["file"].size)
            user_profile.total_used += form.cleaned_data["file"].size
            if user_profile.total_used <= user_profile.upload_limit:
                user_profile.save()
                file.save(os.path.join(current_dir))

    # Showing directory content
    files = UserFile.objects.filter(
        directory=current_dir, owner=request.user.id)

    # Json file list
    tmp_json = serializers.serialize("json", files)
    files_json = json.dumps(json.loads(tmp_json))
    directories_names = [dir for dir in os.listdir(
        absolute_path) if os.path.isdir(os.path.join(absolute_path, dir))]
    print(directories_names)
    for name in directories_names:
        directories.append({'name': name, 'url': os.path.join(path, name)})


    # Breadcrumb
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
        'space': space,
        'upload_error': upload_error,
        'user': request.user,
    })


@login_required()
def download(request, path):
    """Download file when clicking on it"""
    file_path = os.path.join(
        settings.MEDIA_ROOT, path)
    file_path = unquote(file_path)
    if file_path.endswith("/"):
        file_path = file_path[0:-1]
    if os.path.exists(file_path):
        try:
            return FileResponse(open(file_path, 'rb'), os.path.basename(file_path), as_attachment=True)
        except IsADirectoryError:
            return redirect(reverse('files'))
    raise Http404


@login_required
def folder_creation(request, path):
    """Folder creation"""
    name = request.GET.get('dirname')
    if name:
        folder_path = os.path.join(
            settings.MEDIA_ROOT, request.user.username, "files", path, name)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
    return redirect(reverse("files", kwargs={"path": path}))


@login_required
def del_file(request, path):
    """File or folder deletion"""
    redirection = request.GET.get('redirect')
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, path)):
        file = UserFile.objects.get(
            file=path, owner=request.user.id)
        profile = Profile.objects.get(user=request.user.id)
        profile.total_used -= file.size
        profile.save()
        file.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, path))
    else:
        path = os.path.join(settings.MEDIA_ROOT,
                            request.user.username, 'files', path)
        dir_contents = os.listdir(path)
        if len(dir_contents) == 0:
            os.rmdir(path)
        else:
            shutil.rmtree(path)

    return redirect(reverse("files", kwargs={'path': redirection}))


@login_required
def fav(request, path):
    filename = request.GET.get('filename')
    to_file = os.path.join(request.user.username, "files", path)
    file = UserFile.objects.get(file=os.path.join(
        to_file, filename), owner=request.user.id)
    if not file.favorite:
        file.favorite = True
    else:
        file.favorite = False
    file.save(to_file)
    return redirect(reverse('files', kwargs={'path': path}))


@login_required
def fav_list(request):
    files = UserFile.objects.filter(favorite=True, owner=request.user.id)
    return render(request, 'files.html', {
        'directory_files': files,
        'directory_directories': [],
    })


@login_required
def last_files(request):
    files = UserFile.objects.filter(
        owner=request.user.id).order_by("-last_modification")
    return render(request, 'files.html', {
        'directory_files': files,
        'directory_directories': [],
    })
