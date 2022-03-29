from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('add_album/', add_album, name='add_album'),
    path('album/<uuid:album_id>/', show_album, name='album'),
    path('login/', login, name='login'),
    path('photo/<uuid:album_id>/', add_photo, name='photo'),
    path('delete_photo/<pk>/', PhotoDeleteView.as_view(), name='delete_photo'),
    path('add_video/<uuid:photo_id>/', add_video, name='add_video'),
    path('video/', get_list_video, name='video_list'),
    path('video/<uuid:pk>/', get_video, name='video'),
    path('stream/<uuid:pk>/', get_streaming_video, name='stream'),
    path('qrcode/<uuid:album_id>', create_qr_code, name='qrcode'),
]
