from django import template

from main.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


register = template.Library()


@register.simple_tag()
def get_albums(filter=None):
    if not filter:
        return Albums.objects.all()
    else:
        return Albums.objects.filter(pk=filter)


@register.inclusion_tag('main/list_albums.html')
def show_albums(request):
    albums = Albums.objects.all()
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(albums, results)
    page_obj = paginator.get_page(page)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        albums = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        albums = paginator.page(page)

    photo = Media.objects.all()
    return {'album': albums, 'photo': photo, 'paginator': paginator, 'page_obj': page_obj}
