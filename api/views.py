from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AlbumSerializer, MediaSerializer
from main.models import Albums, Media


@api_view(['GET'])
def get_routes(request):

    routes = [
        {'GET': '/api/album'},
        {'GET': '/api/album/id'},
        {'POST': '/api/album/id/vote'},

        {'POST': '/api/projects/token'},
        {'POST': '/api/projects/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
def get_albums(request):
    albums = Albums.objects.all()
    serializer = AlbumSerializer(albums, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_album(request, pk):
    album = Albums.objects.get(id=pk)
    media = Media.objects.filter(album=pk)
    serializer = AlbumSerializer(album, many=False)
    serializer_media = MediaSerializer(media, many=True)
    return Response(serializer.data)
