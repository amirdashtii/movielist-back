from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Cast, Movie, Profile, List, ListItem


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            # to create the object
            return self.get_queryset().create(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ['id', 'full_name']


class MovieSerializer(serializers.ModelSerializer):

    actors = CreatableSlugRelatedField(
        many=True,
        slug_field='full_name',
        queryset=Cast.objects.all()
    )
    director = CreatableSlugRelatedField(
        many=True,
        slug_field='full_name',
        queryset=Cast.objects.all()
    )
    writer = CreatableSlugRelatedField(
        many=True,
        slug_field='full_name',
        queryset=Cast.objects.all()
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'actors', 'director', 'writer', 'orginal_title', 'rated', 'released', 'runtime',
                  'genre', 'plot', 'language', 'country', 'awards', 'poster', 'metascore', 'imdbrating', 'imdbid', 'type']


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'phone', 'birth_date']


class ListItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = ListItem
        fields = ['id', 'movie']


class AddListItemSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, value):
        if not Movie.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No movie with the given ID was found.')
        return value

    def save(self, **kwargs):
        list_id = self.context['list_id']
        movie_id = self.validated_data['movie_id']

        try:
            list_item = ListItem.objects.get(
                list_id=list_id, movie_id=movie_id)
        except ListItem.DoesNotExist:
            self.instance = ListItem.objects.create(
                list_id=list_id, **self.validated_data)
        return self.instance

    class Meta:
        model = ListItem
        fields = ['id', 'movie_id']


class UpdateListItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListItem
        fields = ['movie']


class SampelListItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = ListItem
        fields = ['movie']


class ListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = SampelListItemSerializer(many=True, read_only=True)
    total_movie = serializers.SerializerMethodField()

    def get_total_movie(self, list: list):
        return (list.items.count())

    class Meta:
        model = List
        fields = ['id', 'profile', 'name', 'description', 'items', 'total_movie']
