import json
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from json import JSONEncoder
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
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


class ProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ListViewSet(ModelViewSet):
    # queryset = List.objects.prefetch_related('items__movie').all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return List.objects.prefetch_related('items__movie').all()

        (profile_id, created) = Profile.objects.only(
            'id').get_or_create(user_id=user.id)
        return List.objects.filter(profile_id=profile_id)


class ListItemViwSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class SearchMovie(APIView):
    def post(self, request):
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
        values["actors"] = values["actors"].split(", ")
        values["director"] = values["director"].split(", ")
        values["writer"] = values["writer"].split(", ")
        return Response(values)

