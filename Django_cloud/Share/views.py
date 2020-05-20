from django.shortcuts import render, redirect, get_object_or_404
from .models import ShareLink
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import os.path as p

@login_required
def create_share_link(request, path):
    fs = FileSystemStorage()
    full_path = p.join(request.user.username, 'files', path)
    print(p.join(fs.location, full_path))
    if p.exists(p.join(fs.location, full_path)):
        link = ShareLink(link=ShareLink.link_generation(),
                         file_path=path, creator=request.user)
        link.save()
    return JsonResponse({'link': link.link})

def s(request, file_link):
    link = get_object_or_404(ShareLink, link=file_link)
    return redirect(reverse('download', kwargs={'path': link.file_path}))
