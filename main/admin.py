from django.contrib import admin
from .models import *


class AlbumsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'album', 'video')
    list_display_links = ('id', 'photo', 'video')
    search_fields = ('id',)


# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'photo', 'alb')
#     list_display_links = ('id', 'photo')
#     search_fields = ('id',)
#
#
# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'video', 'image')
#     list_display_links = ('id', 'video')
#     search_fields = ('id',)


admin.site.register(Albums, AlbumsAdmin)
admin.site.register(Media, MediaAdmin)
# admin.site.register(Image, ImageAdmin)
# admin.site.register(Video, VideoAdmin)
