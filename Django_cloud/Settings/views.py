from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from Auth.models import Profile
from django.contrib.auth.models import User

@login_required
def main(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        uform = UserForm(request.POST, instance=user)
        pform = ProfileForm(request.POST)

        if uform.is_valid() and pform.is_valid():
            profile = Profile.objects.get(user=user.id)
            user.username = uform.cleaned_data['username']
            user.first_name = uform.cleaned_data['first_name']
            user.last_name = uform.cleaned_data['last_name']
            user.email = uform.cleaned_data['email']
            profile.theme = pform.cleaned_data['theme']

            user.save()
            profile.save()

    else:
        profile = Profile.objects.get(user=request.user.id)
        uform = UserForm(initial={'username': request.user.username,
                                    'first_name': request.user.first_name,
                                    'last_name': request.user.last_name,
                                    'email': request.user.email},
                                instance=request.user)
        pform = ProfileForm(initial={'theme': profile.theme})

    return render(request, 'settings/index.html', {
        'uform': uform,
        'pform': pform,
    })
