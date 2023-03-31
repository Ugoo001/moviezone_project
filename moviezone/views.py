from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

# Create your views here.
@api_view(['GET'])
def recommend_movies(request):
    # Get genre,title and ratings
    title = request.GET.get('title')
    genres = request.GET.get('genres')
    user_rating = request.GET.get('user_rating')

    imdb_api_key = 'k_026vx761'
    imdb_url = f'https://imdb-api.com/API/AdvancedSearch/{imdb_api_key}?'
    if title:
        imdb_url += f'title={title}&'
    if genres:
        imdb_url += f'genres={genres}&'
    if user_rating:
        imdb_url += f'user_rating={user_rating}&'
    imdb_response = requests.get(imdb_url)
    imdb_data = imdb_response.json()
    

    #sorting the movies in descending order
    if imdb_data['results'] is not None:
        sort_movies = sorted(imdb_data['results'], key=lambda k: float(k['imDbRating']) if k.get('imDbRating') is not None else -1, reverse=True)

    #checking recommended movie on netflix
        if sort_movies:
            recommended_movie = sort_movies[0]['title']
            recommended_movie_url = recommended_movie.replace(" ", "+")
        
            netflix_url = f'https://www.netflix.com/search?q={recommended_movie_url}'
            netflix_response = requests.get(netflix_url)
            if netflix_response.status_code == 200:
                return Response({'name': recommended_movie, 'url': netflix_url})
            else:
                return Response({'message': f'Your recommended movie is {recommended_movie}. Movie is not available on netflix'})
    else:
        return Response({'message': 'No movies found with the given criteria'})    

