from django.shortcuts import render, redirect, get_object_or_404
from .models import ShareLink
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from Files.file_utils import recursive_file_list
from Files.views import FileView
import os.path as p
from io import BytesIO
import zipfile
from django.views import View

@login_required
def create_share_link(request, path):
    fs = FileSystemStorage()
    full_path = p.join(request.user.username, 'files', path)
    if p.exists(p.join(fs.location, full_path)):
        link = ShareLink(link=ShareLink.link_generation(),
                         file_path=path, creator=request.user)
        link.save()
        return JsonResponse({'link': link.link})
    else:
        raise Http404

class ShareDownloadView(View, FileView):
    def get(self, request, file_link):
        link = get_object_or_404(ShareLink, link=file_link)
        to_send = p.join(link.creator.username, "files", link.file_path)
        if p.exists(p.join(self.fs.location, to_send)):
            # Send file or folder if exists
            # Compress all folder into zip and return it
            if p.isdir(p.join(self.fs.location, to_send)):
                filenames = recursive_file_list(
                    p.join(self.fs.location, to_send))
                zip_filename = f"{p.basename(to_send)}.zip"
                s = BytesIO()
                zf = zipfile.ZipFile(s, "w")
                for fpath in filenames:
                    fdir, fname = p.split(fpath)
                    zf.write(fpath, fpath.replace(p.join(
                        self.fs.location, link.creator.username, 'files'), ''))
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
