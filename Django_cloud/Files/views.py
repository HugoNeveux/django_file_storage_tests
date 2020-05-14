import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UserFile
from Auth.models import Profile
from django.conf import settings
from django.http import Http404, FileResponse, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from urllib.parse import unquote
from django.shortcuts import get_object_or_404
import json
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from .file_utils import format_bytes, recursive_file_list
import shutil
from io import BytesIO
import zipfile

class AjaxResponsibleMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class FileUploadAndListView(AjaxResponsibleMixin, LoginRequiredMixin, FormView):
    """Read ans save sent file"""
    form_class = UploadFileForm
    template_name = 'files.html'

    def post(self, request, *args, **kwargs):
        path = request.POST.get('path', None)
        # Variables and file storage initialisation
        current_dir = os.path.join(request.user.username, "files", path)
        absolute_path = os.path.join(settings.MEDIA_ROOT, current_dir)
        files = []
        directories = []
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            # Space available
            user_profile = Profile.objects.get(user=request.user.id)
            space_available = user_profile.upload_limit - user_profile.total_used
            for file in files:
                if file.size > space_available:
                    return JsonResponse({'error': f'Limite de stockage dépassée: le fichier {file.name} ne peut pas être enregistré.'},
                                        status=400)
                else:
                    existing_file = UserFile.objects.filter(
                        directory=current_dir, owner=request.user.id, name=request.FILES['file'].name)
                    if existing_file.count() > 0:
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

            return JsonResponse({'form': True})
        else:
            # return JsonResponse({'form': False})
            return JsonResponse(form.errors, status=400)


    def get(self, request, path='', *args, **kwargs):
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

        # Showing directory content
        files = UserFile.objects.filter(
            directory=current_dir, owner=request.user.id)

        # Json file list
        tmp_json = serializers.serialize("json", files)
        files_json = json.dumps(json.loads(tmp_json))
        directories_names = [dir for dir in os.listdir(
            absolute_path) if os.path.isdir(os.path.join(absolute_path, dir))]
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

        # Preparing context
        return render(request, 'files.html', {
            'form': self.get_form_class(),
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
def download_dir(request, path):
    """Download dir"""
    dir_path = os.path.join(
        settings.MEDIA_ROOT, request.user.username, "files", path)
    dir_path = unquote(dir_path)
    if dir_path.endswith("/"):
        dir_path = dir_path[0:-1]
    if os.path.isdir(dir_path):  # Compress all folder into zip and return it
        filenames = recursive_file_list(dir_path)
        zip_filename = f"{dir_path.split('/')[-1]}.zip"
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        for fpath in filenames:
            fdir, fname = os.path.split(fpath)

            zf.write(fpath, fpath.replace(os.path.join(settings.MEDIA_ROOT, request.user.username, 'files'), ''))
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return resp
    raise Http404

@login_required()
def download_file(request, id):
    """Download file"""
    file = get_object_or_404(UserFile, id=id)
    if request.user == file.owner:
        return FileResponse(open(file.file.path, 'rb'), file.name, as_attachment=True)
    raise PermissionDenied

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


@login_required
def mv(request):
    """Moves file from origin to dest"""
    origin = request.GET.get('from')
    dest = request.GET.get('to')
    full_dest = os.path.join(request.user.username, 'files', dest)
    file_origin = os.path.join(request.user.username, 'files', origin)
    print(file_origin)
    moved_file = get_object_or_404(UserFile, owner=request.user, file=file_origin)
    if os.path.isdir(os.path.join(settings.MEDIA_ROOT, full_dest)):
        os.rename(os.path.join(settings.MEDIA_ROOT, file_origin),
                  os.path.join(settings.MEDIA_ROOT, full_dest, moved_file.name))
        moved_file.file = os.path.join(full_dest, moved_file.name)
        moved_file.directory = full_dest
        print(moved_file.file)
        moved_file.save(upload_to=full_dest)
        return redirect(reverse('files', kwargs={'path': ''}))
    return Http404
