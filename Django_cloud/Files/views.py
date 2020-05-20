import os
from os import path as p
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import FavoriteFiles, RecentFiles
from Auth.models import Profile
from django.conf import settings
from django.http import Http404, FileResponse, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from urllib.parse import unquote, quote
from django.shortcuts import get_object_or_404
import json
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from django.template.loader import render_to_string
from .file_utils import format_bytes, recursive_file_list
import shutil
from io import BytesIO
import zipfile


class FileView():
    fs = FileSystemStorage()


class TreeView(LoginRequiredMixin, FormView, FileView):
    """
    Shows all files & folders contained in current file and
    allows file upload
    """
    form_class = UploadFileForm
    template_name = 'files.html'

    def post(self, request, *args, **kwargs):
        """
        Post function for /Files/ or /Files/tree/. Takes two arguments :
        path (for upload path) and file (uploaded file). Saves file to
        filesystem
        """
        # Store GET arguments
        path = request.POST.get('path', None)

        # Variables initialisation
        current_dir = p.join(request.user.username, "files", path)
        form = self.get_form(self.get_form_class())
        files = request.FILES.getlist('file')
        if form.is_valid():
            # Space available
            user_profile = Profile.objects.get(user=request.user.id)
            space_available = user_profile.upload_limit - user_profile.total_used
            # Default success response
            res = {'form': True, 'space_used': format_bytes(
                user_profile.total_used)}

            for file in files:
                if file.size > space_available:
                    # Error if there isn't enough place to store file
                    return JsonResponse({'error': f'Limite de stockage dépassée: le fichier {file.name} ne peut pas être enregistré.'},
                                        status=400)
                else:
                    if not p.exists(p.join(self.fs.location, current_dir, file.name)):
                        # Create file object for render and update response
                        res['file_html'] = render_to_string('files_templates/ul_file.html', {
                            'file': {'name': file.name, 'url': p.join(
                                path, file.name), 'favorite': False},
                            'current_dir': path,
                        })
                        # Increase used space
                        user_profile.total_used += file.size
                        user_profile.save()
                        MAX_RECENT_FILES = 50
                        if RecentFiles.objects.filter(owner=request.user).count() >= MAX_RECENT_FILES - 1:
                            delta = RecentFiles.objects.filter(owner=request.user).count() - (MAX_RECENT_FILES - 1)
                            print(delta)
                            for entry in RecentFiles.objects.filter(owner=request.user).order_by('last_modification')[:delta]:
                                entry.delete()
                        RecentFiles(owner=request.user, path=p.join(path, file.name)).save()
                    else:
                        print(p.join(path, file.name))
                        RecentFiles.objects.get(owner=request.user, path=p.join(path, file.name)).save()
                    with open(p.join(self.fs.location, current_dir, file.name), 'wb+') as dest_file:
                        # Saving file
                        for chunk in file.chunks():
                            dest_file.write(chunk)

            return JsonResponse(res)
        else:
            return JsonResponse(form.errors, status=400)

    def get(self, request, path='', *args, **kwargs):
        """
        Response to get request to /Files/ or /Files/tree/,
        shows a list of files and directories contained in the current dir.
        If no argument provided, showing user root folder
        """
        # Variables and file storage initialisation
        current_dir = os.path.join(request.user.username, "files", path)
        f_objects, d_objects = [], []

        # Space available
        user_profile = Profile.objects.get(user=request.user.id)
        space = {"available": format_bytes(user_profile.upload_limit),
                 "used": format_bytes(user_profile.total_used),
                 "available_b": user_profile.upload_limit - user_profile.total_used}

        # Showing directory content by creating dictionaries for each file &
        # dir
        for name in self.fs.listdir(current_dir)[1]:
            f_objects.append({'name': name, 'url': os.path.join(path, name),
                              'favorite': False})

        for name in self.fs.listdir(current_dir)[0]:
            d_objects.append(
                {'name': name, 'url': os.path.join(path, name)})

        # Json file list
        files_json = json.dumps(f_objects)

        # Breadcrumb preparation
        breadcrumb = {}
        full_path = path.split(os.sep)
        breadcrumb["path"] = []
        to_dir = ""
        for dir in full_path[:-1]:
            to_dir = os.path.join(to_dir, dir)
            breadcrumb["path"].append([dir, to_dir])

        breadcrumb["active"] = full_path[-1]

        # Preparing context
        return render(request, 'files_templates/files.html', {
            'form': self.get_form(),
            'directory_files': f_objects,
            'directory_directories': d_objects,
            'breadcrumb': breadcrumb,
            'files_json': files_json,
            'current_dir': path,
            'space': space,
            'user': request.user,
        })


class DownloadView(LoginRequiredMixin, View, FileView):
    def get(self, request, path, *args, **kwargs):
        """
        Sends a FileResponse with a zip file representing requested dir,
        or a single file for a single-file download
        """
        path = unquote(path)
        to_send = p.join(request.user.username, "files", path)
        if to_send.endswith('/'):
            to_send = to_send[0:-1]
        if p.exists(p.join(self.fs.location, to_send)):
            # Send file or folder if exists
            # Compress all folder into zip and return it
            if p.isdir(p.join(self.fs.location, to_send)):
                filenames = recursive_file_list(
                    p.join(self.fs.location, to_send))
                zip_filename = f"{to_send.split('/')[-1]}.zip"
                s = BytesIO()
                zf = zipfile.ZipFile(s, "w")
                for fpath in filenames:
                    fdir, fname = os.path.split(fpath)

                    zf.write(fpath, fpath.replace(os.path.join(
                        settings.MEDIA_ROOT, request.user.username, 'files'), ''))
                zf.close()
                resp = HttpResponse(
                    s.getvalue(), content_type="application/x-zip-compressed")
                resp['Content-Disposition'] = f'attachment; filename={zip_filename}'
                return resp
            else:
                # Open and send file
                file = self.fs.open(to_send, 'rb')
                return FileResponse(file, file.name, as_attachment=True)
                file.close()
        else:
            raise Http404   # Return HTTP 404 error


class FolderCreationView(LoginRequiredMixin, View, FileView):
    def get(self, request, path):
        """Folder creation"""
        next = request.GET.get('next')
        dir_path = p.join(self.fs.location,
                          request.user.username, 'files', path.strip())
        if not p.exists(dir_path):
            os.mkdir(dir_path)
        return redirect(reverse("files", kwargs={"path": next}))


class DeleteFileView(LoginRequiredMixin, View, FileView):
    def get(self, request, path):
        """
        Delete a file or a folder using one argument : the element path
        """
        next = request.GET.get('next')  # Redirection URL
        path_to = p.join(request.user.username, 'files', path)
        if os.path.isfile(p.join(self.fs.location, path_to)):
            profile = Profile.objects.get(user=request.user.id)
            profile.total_used -= self.fs.size(path_to)
            # Delete potential database entries
            if FavoriteFiles.objects.filter(owner=request.user, path=path).count() > 0:
                FavoriteFiles.objects.get(owner=request.user, path=path).delete()
            if RecentFiles.objects.filter(owner=request.user, path=path).count() > 0:
                RecentFiles.objects.get(owner=request.user, path=path).delete()
            profile.save()
            self.fs.delete(path_to)
        elif p.isdir(p.join(self.fs.location, path_to)) and path != "":
            to_dir = p.join(self.fs.location, path_to)
            if len(self.fs.listdir(path_to)) == 0:
                os.rmdir(to_dir)
            else:
                shutil.rmtree(to_dir)
        return redirect(reverse("files", kwargs={'path': next if next is not None else ''}))


class FavFileView(LoginRequiredMixin, View):
    def get(self, request, path):
        next = request.GET.get('next')
        existing = FavoriteFiles.objects.filter(path=path, owner=request.user)
        if existing.count() > 0:
            existing.delete()
        else:
            FavoriteFiles(path=p.join(path), owner=request.user).save()
        return redirect(reverse('files', kwargs={'path': next if next is not None else ''}))


class FavFileListView(LoginRequiredMixin, View, FileView):
    def get(self, request):
        favs = FavoriteFiles.objects.filter(owner=request.user)
        files = []
        for element in favs:
            if p.isfile(p.join(self.fs.location, request.user.username, 'files', element.path)):
                files.append({'name': p.basename(element.path), 'url': element.path,
                              'favorite': True})
        return render(request, 'files_templates/files.html', {
            'directory_files': files,
            'directory_directories': [],
        })


class LastFilesView(LoginRequiredMixin, View, FileView):
    def get(self, request):
        f_objects = []
        for file in RecentFiles.objects.filter(owner=request.user).order_by("-last_modification"):
            fav = FavoriteFiles.objects.filter(
                owner=request.user, path=file.path).count() > 0
            f_objects.append({'name': p.basename(file.path),
                         'url': file.path, 'favorite': fav})
        return render(request, 'files_templates/files.html', {
            'directory_files': f_objects,
            'directory_directories': [],
        })


class MoveFileView(LoginRequiredMixin, View, FileView):
    def get(self, request):
        """Moves file from origin to dest"""
        origin = request.GET.get('from')
        dest = request.GET.get('to')
        file_origin = p.join(request.user.username, 'files', origin)
        if dest == 'previous':
            full_dest = p.join(p.dirname(p.dirname(file_origin)))
        else:
            full_dest = p.join(request.user.username, 'files', dest)
        if not full_dest.startswith(p.join(request.user.username, 'files')):
            full_dest = os.path.join(request.user.username, 'files')
        if p.isdir(p.join(self.fs.location, full_dest)) and p.exists(p.join(self.fs.location, file_origin)):
            os.rename(p.join(self.fs.location, file_origin),
                      p.join(self.fs.location, full_dest, p.basename(file_origin)))
            return redirect(reverse('files', kwargs={'path': request.GET.get('next')}))
        return Http404
