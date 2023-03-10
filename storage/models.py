from django.conf import settings
from django.contrib import admin
from django.db import models
from uuid import uuid4


class Cast(models.Model):
    full_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        ordering = ['full_name']


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Movie(models.Model):
    title = models.CharField(max_length=255)
    orginal_title = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    to_year = models.IntegerField(null=True, blank=True)
    rated = models.CharField(max_length=255, null=True, blank=True)
    released = models.CharField(max_length=255, null=True, blank=True)
    runtime = models.CharField(max_length=255, null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='genre')
    director = models.ManyToManyField(
        Cast, blank=True, related_name='directors')
    writer = models.ManyToManyField(
        Cast, blank=True, related_name='writers')
    actors = models.ManyToManyField(
        Cast, blank=True, related_name='actors')
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    awards = models.TextField(null=True, blank=True)
    poster = models.URLField(max_length=200, null=True, blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    imdbrating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True)
    imdbid = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Profile(models.Model):
    phone = models.CharField(null=True, blank=True, max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ListItem(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.PROTECT, related_name='items')
    movie = models.ForeignKey(
        Movie, on_delete=models.PROTECT, related_name='listitems')

    class Meta:
        unique_together = [['list', 'movie']]