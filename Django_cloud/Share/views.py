from django.shortcuts import render
from .models import ShareLink
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse

@login_required
def create_share_link(request, file_id):
    fs = FileSystemStorage()
    if request.user == file.owner:
        link = ShareLink(link=ShareLink.link_generation(),
                         path=file, creator=request.user)
        link.save()
    return JsonResponse({'link': link.link})

def s(request, file_link):
    link = get_object_or_404(ShareLink, link=file_link)
    file = get_object_or_404(UserFile, id=link.to_file.id)
    return FileResponse(open(file.file.path, 'rb'), file.name, as_attachment=True)
