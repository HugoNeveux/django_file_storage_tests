from django import template
from Auth.models import Profile

register = template.Library()

@register.filter(name='has_dark')
def has_dark(user):
    p = Profile.objects.get(user=user)
    return True if p.theme == 2 else False
