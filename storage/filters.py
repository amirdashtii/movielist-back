from django_filters.rest_framework import FilterSet
from .models import Movie, ListItem


class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'actors__full_name': ['exact'],
            'director__full_name': ['exact'],
            'writer__full_name': ['exact'],
            'genre__name': ['exact'],
            'year': ['gte', 'lte'],
        }


class ListItemFilter(FilterSet):
    class Meta:
        model = ListItem
        fields = {
            'movie__actors__full_name': ['exact'],
            'movie__director__full_name': ['exact'],
            'movie__writer__full_name': ['exact'],
            'movie__genre__name': ['exact'],
            'movie__year': ['gte', 'lte'],
            'movie__type': ['exact'],
        }
