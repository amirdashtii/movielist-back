from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Cast, Movie, Profile

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    list_per_page: 10
    ordering = ['full_name']
    search_fields = ['full_name__istartswith']

    @admin.display(ordering='movie_count')
    def movie_count(self, cast):
        url = (
            reverse('admin:storage_movie_changelist')
            + '?'
            + urlencode({
                "cast__id": str(cast.id)
            }))
        return format_html('<a href="{}"//">{}</a>', url, cast.movie_count)

    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         movie_count=Count('movie')
    #     )

   
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    autocomplete_fields = ['actor','director','writer']
    list_display = ['title', 'year']
    list_per_page: 10
    ordering = ['title', 'year']
    search_fields = ['title__istartswith', 'year__istartswith']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_per_page: 10
    ordering = ['first_name', 'last_name']
    
