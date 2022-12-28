from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("movies", views.MovieViewSet, basename='movies')
router.register("casts", views.CastViewSet, basename='casts')


urlpatterns = [
    path('add-movie-to-list/', views.add_movie_to_list),
    path('find-movie/', views.FindMovie.as_view()),
]
# URLConf
urlpatterns += router.urls


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('add-movie-to-list/', views.add_movie_to_list),
#     path('find-movie/', views.FindMovie.as_view()),
#     # path('find-movie/', views.find_movie),
#     # path('cast/', views.CastViewSet.as_view()),
#     # path('movies/', views.MovieViewSet.as_view()),
#     # path('profile/', views.ProfileViewSet.as_view()),
# ]
