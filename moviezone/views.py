from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
import requests
import os
# Create your views here.
@cache_page(3600) # Cache the response for 1 hour (60*60)
@api_view(['GET'])
def recommend_movies(request):
    # Get genre,title and ratings
    try:
        title = request.GET.get('title')
        genres = request.GET.get('genres')
        user_rating = request.GET.get('user_rating')

        imdb_api_key = 'k_i13l1c3r' #add api key here from imdb api
        imdb_url = f'https://imdb-api.com/API/AdvancedSearch/{imdb_api_key}?'
        if title:
            imdb_url += f'title={title}&'
        if genres:
            imdb_url += f'genres={genres}&'
        if user_rating:
            imdb_url += f'user_rating={user_rating}&'
    
        if not genres and not title and not user_rating:
            return Response({'message': 'Add a valid parameter, genres,title or user_rating'})
        imdb_response = requests.get(imdb_url)
        imdb_data = imdb_response.json()
    

    #sorting the movies in descending order
        if imdb_data['results'] is not None:
            sort_movies = sorted(imdb_data['results'], key=lambda k: float(k['imDbRating']) if k.get('imDbRating') is not None else -1, reverse=True)

    #checking recommended movie on netflix
            if sort_movies:
                recommend_movie_image = sort_movies[0]['image']
                recommend_movie_plot = sort_movies[0]['plot']
                recommended_movie = sort_movies[0]['title']
                recommended_movie_url = recommended_movie.replace(" ", "+")
        
                netflix_url = f'https://www.netflix.com/search?q={recommended_movie_url}'
                netflix_response = requests.get(netflix_url)
                if netflix_response.status_code == 200:
                    return Response({'name': recommended_movie, 'url': netflix_url, 'image':recommend_movie_image, 'plot': recommend_movie_plot})
                else:
                    return Response({'message': f'Your recommended movie is {recommended_movie}. Movie is not available on netflix', 'image': recommend_movie_image, 'plot': recommend_movie_plot})
        else:
            return Response({'message': 'No movies found with the given criteria'})    

    except Exception as e:
        return Response({'message': f'Error: {str(e)}'})