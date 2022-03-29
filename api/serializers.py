from rest_framework import serializers
from main.models import Albums, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)

    class Meta:
        model = Albums
        fields = '__all__'



