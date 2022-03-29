from pathlib import Path
from typing import IO, Generator
from django.http import HttpResponseNotFound, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from .forms import *
from .models import *
import qrcode


menu = [
    {'title': 'Добавить альбом', 'url_name': 'add_album'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Войти', 'url_name': 'login'}
]


def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница',
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    return render(request, 'main/about.html', {'menu': menu, 'title': 'О сайте'})


def add_album(request):
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddAlbumForm()
    return render(request, 'main/add_album.html', {'form': form, 'menu': menu, 'title': 'Добавить альбом'})


def login(request):
    return HttpResponse("Авторизация")


def show_album(request, album_id):
    album = get_object_or_404(Albums, pk=album_id)
    photo = Media.objects.filter(album=album_id)
    context = {
        'album': album,
        'menu': menu,
        'title': album.title,
        'photo': photo,

    }
    return render(request, 'main/album.html', context=context)


def add_photo(request, album_id):
    album = get_object_or_404(Albums, pk=album_id)
    if request.method == 'POST':
        form = AddMediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo', album_id)
    else:
        form = AddMediaForm(initial={'album': album})

    context = {
        'album': album,
        'form': form,
        'menu': menu,
        'title': 'Добавить фото',
    }
    return render(request, 'main/add_photo.html', context=context)


def add_video(request, photo_id):
    media = get_object_or_404(Media, pk=photo_id)

    if request.method == 'POST':
        form = AddMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media.video = request.FILES.get("video")
            media.save()
            return redirect('home')
    else:
        form = AddMediaForm(initial={'album': media.album, 'media': media.photo})

    context = {
        'media': media,
        'form': form,
        'menu': menu,
        'title': 'Добавить видео'
    }
    return render(request, 'main/add_video.html', context=context)


class PhotoDeleteView(DeleteView):
    model = Media
    success_url = '/'
    template_name = 'main/photo_delete.html'


def get_list_video(request):
    return render(request, 'main/my_video.html', {'video_list': Media.objects.exclude(video='')})


def get_video(request, pk: int):
    _media = get_object_or_404(Media, id=pk)
    return render(request, 'main/video.html', {'video': _media})


def create_qr_code(request, album_id: int):
    data = f'http://127.0.0.1:8000/album/{album_id}'
    print(data)

    img_name = f'{album_id}.png'
    print(img_name)
    img = qrcode.make(data)
    img.save(f'media/QR_code/{img_name}')
    return HttpResponse('<h1>Qr code Create</h1>')


def ranged(file: IO[bytes], start: int = 0, end: int = None, block_size: int = 8192,) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, video_pk: int) -> tuple:
    _video = get_object_or_404(Media, pk=video_pk)

    path = Path(_video.video.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'
    return file, status_code, content_length, content_range


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/')
    response['Accept-Ranges'] = ['bytes']
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def page_not_found(request, exception):
    if request.POST:
        print(request.POST)
    return HttpResponseNotFound(f'<h1>Page not found!!!</h1><p>{exception}</p>')
