from django.db import models
from uuid import uuid4

class Cast(models.Model):
    full_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        ordering = ['full_name']


class Movie(models.Model):
    title = models.CharField(max_length=255)
    orginal_title = models.CharField(max_length=255, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    rated = models.CharField(max_length=255, null=True, blank=True)
    released = models.CharField(max_length=255, null=True, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
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
    metascore = models.PositiveIntegerField(null=True, blank=True)
    imdbrating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True)
    imdbid = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name']

class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class ListItem(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.PROTECT, related_name='items')
    movie = models.ForeignKey(
        Movie, on_delete=models.PROTECT, related_name='listitems')

    class Meta:
        unique_together=[['list','movie']]

