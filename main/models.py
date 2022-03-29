from django.db import models
from django.urls import reverse
import uuid


class Albums(models.Model):
    title = models.CharField(max_length=255, blank=True, default='Без названия', verbose_name='Название')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последние обновление')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_id': self.pk})

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['time_create', 'title']


class Media(models.Model):
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, verbose_name='Альбом', related_name='media')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', verbose_name='изображение', blank=True)
    video = models.FileField(upload_to='video/%Y/%m/%d', verbose_name='Видео', blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = 'Медиа'
        verbose_name_plural = 'Медиа'
        ordering = ['id']
