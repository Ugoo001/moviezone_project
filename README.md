# moviezone_project
Moviezone Project
Moviezone is a Django-based web application that provides movie recommendations based on user input criteria such as title, genre, and user rating. It also checks if the recommended movie is available on Netflix and provides additional information like the movie's plot and trailer.


Before running the Moviezone application, make sure you have the following software and resources installed:
Python 3.7 or later
Django 2.2 or later
Django REST framework
Requests library (for making HTTP requests)

Install the required Python packages using pip.

pip install -r requirements.txt
Add your IMDb API key to views.py. Replace the imdb_api_key variable with your own IMDb API key.

Run the Django development server.

Usage
API Endpoint
The Moviezone API provides a single endpoint for recommending movies:

Endpoint: /movies/
Parameters
You can make GET requests to the /movies/ endpoint with the following query parameters:

title: The title of the movie.
genres: The genre of the movie.
user_rating: The user rating of the movie.
You can use one or more of these parameters to filter and get movie recommendations.

Response
The API response will include information about the recommended movie, including its availability on Netflix (if applicable), plot, trailer, and more. The response is in JSON format and may look like this:

json
Copy code
{
    "name": "Recommended Movie Title",
    "url": "Netflix URL",
    "image": "Movie Poster Image URL",
    "plot": "Movie Plot Summary",
    "trailer": "Movie Trailer URL",
    "trailer_embed": "Embedded Trailer Link",
    "thumbnail": "Trailer Thumbnail URL"
}
If the recommended movie is not available on Netflix, the response will indicate that.

Caching
The API response is cached for 1 hour (3600 seconds) to reduce the load on external APIs. The cache can be adjusted by modifying the @cache_page decorator in views.py.

Error Handling
The application includes error handling to catch and display any exceptions that may occur during the process. If an error occurs, the API response will include an error message.

API Key
To use the IMDb API, you need to obtain an API key from IMDb. Add your own API key in the imdb_api_key variable within the views.py file.

Contributing
Contributions to the Moviezone project are welcome. If you have any suggestions, bug fixes, or improvements, please create a pull request. Ensure that your code adheres to the project's coding standards and guidelines.

License
This project is licensed under the MIT License. 
