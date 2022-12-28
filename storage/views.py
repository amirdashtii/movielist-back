import json
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from json import JSONEncoder
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import MovieFilter
from .models import Cast, Movie, Profile, List, ListItem
from .pagination import DefaultPagination
from .serializers import CastSerializer, MovieSerializer, ProfileSerializer, ListSerializer, ListItemSerializer, AddListItemSerializer, UpdateListItemSerializer
from movielist import config


class CastViewSet(ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'actors__full_name',
                     'director__full_name', 'writer__full_name']
    ordering_fields = ['title', 'actors__full_name',
                       'director__full_name', 'writer__full_name']


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ListViewSet(ModelViewSet):
    queryset = List.objects.prefetch_related('items__movie').all()
    serializer_class = ListSerializer


class ListItemViwSet(ModelViewSet):
    http_method_names = ['get', 'post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddListItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateListItemSerializer
        return ListItemSerializer

    def get_serializer_context(self):
        return {'list_id': self.kwargs['list_pk']}

    def get_queryset(self):
        return ListItem.objects.filter(list_id=self.kwargs['list_pk']).select_related('movie')


# @csrf_exempt
@api_view(['POST'])
def search_movie(request):
    title = request.POST.get('title')
    year = request.POST.get('year')
    apikey = config.apikey
    url = 'http://www.omdbapi.com/'
    payload = {'s': title, 'y': year, 'r': 'json', 'apikey': apikey}
    result = requests.get(url, params=payload).json()
    return Response(result)


class FindMovie(APIView):
    def post(self, request):
        imdbid = request.POST.get('imdbid')
        title = request.POST.get('title')
        year = request.POST.get('year')
        apikey = config.apikey
        url = 'http://www.omdbapi.com/'
        payload = {'i': imdbid, 't': title, 'y': year,
                   'plot': 'full', 'r': 'json', 'apikey': apikey}
        result = requests.get(url, params=payload).json()
        values = {k.lower(): v for k, v in result.items()
                  } if result['Response'] == 'True' else result['Error']
        values["runtime"] = values["runtime"].replace(' min', '')
        return Response(values)

# @api_view(['POST'])
# def find_movie(request):
#     imdbid = request.POST.get('imdbid')
#     title = request.POST.get('title')
#     year = request.POST.get('year')
#     apikey = config.apikey
#     url = 'http://www.omdbapi.com/'
#     payload = {'i': imdbid, 't': title, 'y': year,
#                'plot': 'full', 'r': 'json', 'apikey': apikey}
#     result = requests.get(url, params=payload).json()
#     values = {k.lower(): v for k, v in result.items()
#               } if result['Response'] == 'True' else result['Error']
#     values["runtime"] = values["runtime"].replace(' min', '')
#     return Response(values)


# @csrf_exempt
@api_view(['POST'])
def add_movie_to_list(request):
    print(request)

    # movie = find_movie(request)
    # serializer = MovieSerializer(data=request.data)
    # serializer.validated_data
    # return Response(request)

    print(movie.content, '-----------')

    # actors = movie['actors'].split(", ")
    # print(actors)

    # myobj = {'full_name': 'amiraaaa'}
    # aaa = {'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMzA2NzkwLCJqdGkiOiI0NTAwZmUwMzQxZDQ0MWViYjFlZjU0YWJmYmE3Yjg1YSIsInVzZXJfaWQiOjF9.KbmINiv3uCEG9Ca3VwdPwSOtjn7KdWp-HU4FdAu0dl4'}
    # requests.post('http://127.0.0.1:8000/storage/actor/', data=myobj, headers=aaa)

    # return ActorViewSet.as_view()(request, actors[0])

    # for actor in actors:
    #     actor,created = Actor.objects.get_or_create(full_name=actor)
    # print(actor)
    # print(movie['director'])
    # print(movie['writer'])
    return movie
