from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from dotenv import load_dotenv, find_dotenv
import requests
import os
# Create your views here.

load_dotenv(find_dotenv())
@cache_page(3600) # Cache the response for 1 hour (60*60)
@api_view(['GET'])
def recommend_movies(request):
    # Get genre,title and ratings
    try:

        title = request.GET.get('title')
        genres = request.GET.get('genres')
        user_rating = request.GET.get('user_rating')

        imdb_api_key = os.getenv("API_KEY") #add api key here from imdb api
        imdb_url = f'https://imdb-api.com/API/AdvancedSearch/{imdb_api_key}?'
        if title:
            imdb_url += f'title={title}&'
        if genres:
            imdb_url += f'genres={genres}&'
        if user_rating:
            imdb_url += f'user_rating={user_rating}&'
    
        if not genres and not title and not user_rating:
            return Response({'message': 'Add a valid parameter, genres,title or user_rating'})
        if genres and title and user_rating == None:
            return Response({'message': 'Invalid input.'})
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

                recommend_movie_id = sort_movies[0]['id']
                recommend_movie_trailer_url = f'https://imdb-api.com/en/API/Trailer/{imdb_api_key}/{recommend_movie_id}'
                trailer_response = requests.get(recommend_movie_trailer_url)
                trailer_data = trailer_response.json()
                
                if trailer_data is not None:
                    recommend_movie_trailer = trailer_data['link']
                    trailer_embed_link = trailer_data['linkEmbed']
                    trailer_thumbnail = trailer_data['thumbnailUrl']
                    
        
                netflix_url = f'https://www.netflix.com/search?q={recommended_movie_url}'
                netflix_response = requests.get(netflix_url)
                if netflix_response.status_code == 200:
                    return Response({'name': recommended_movie,
                                      'url': netflix_url, 
                                      'image':recommend_movie_image, 
                                      'plot': recommend_movie_plot,
                                      'trailer': recommend_movie_trailer,
                                      'trailer_embed': trailer_embed_link,
                                      'thumbnail': trailer_thumbnail,})
                else:
                    return Response({'message': f'Your recommended movie is {recommended_movie}. Movie is not available on netflix', 
                                     'image': recommend_movie_image, 
                                     'plot': recommend_movie_plot,
                                     'trailer': recommend_movie_trailer,
                                     'trailer_embed': trailer_embed_link,
                                     'thumbnail': trailer_thumbnail,})
        else:
            return Response({'message': 'No movies found with the given criteria'})    
            
    except Exception as e:
        return Response({'message': f'Error: {str(e)}'})
