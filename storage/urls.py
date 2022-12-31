from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("movies", views.MovieViewSet, basename='movies')
router.register("casts", views.CastViewSet, basename='casts')
router.register("lists", views.ListViewSet, basename='lists')
router.register("profiles", views.ProfileViewSet)

lists_router = routers.NestedDefaultRouter(router, 'lists', lookup='list')
lists_router.register('items', views.ListItemViwSet, basename='list-items')


urlpatterns = [
    path('search-movie/', views.SearchMovie.as_view()),
    path('find-movie/', views.FindMovie.as_view()),
]

urlpatterns = urlpatterns + router.urls + lists_router.urls
