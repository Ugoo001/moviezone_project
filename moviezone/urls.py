from django.urls import path
from .views import recommend_movies


urlpatterns =[
    path('movies/', recommend_movies, name= 'recommend_movies'),

]