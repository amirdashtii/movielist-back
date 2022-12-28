from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Cast, Movie, Profile


# class CreatableSlugRelatedField(serializers.SlugRelatedField):
#     def to_internal_value(self, data):
#         try:
#             return self.get_queryset().get(**{self.slug_field: data})
#         except ObjectDoesNotExist:
#             # to create the object
#             return self.get_queryset().create(**{self.slug_field: data})
#         except (TypeError, ValueError):
#             self.fail('invalid')


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ['id', 'full_name']


class MovieSerializer(serializers.ModelSerializer):

    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='full_name'
    )
    director = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='full_name'
    )
    writer = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='full_name'
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'actors', 'director', 'writer', 'orginal_title', 'rated', 'released', 'runtime',
                  'genre', 'plot', 'language', 'country', 'awards', 'poster', 'metascore', 'imdbrating', 'imdbid', 'type']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name']
