from django import forms
from django.shortcuts import get_object_or_404

from .models import *


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Albums
        fields = ['title', ]
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'})}


class AddMediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['album', 'photo', 'video']


# class AddImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['alb', 'photo']
#
#
# class AddVideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ['image', 'video']
