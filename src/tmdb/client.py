import requests
from django.conf import settings

tmdb_api = settings.TMDB_API_KEY
def get_headers():
    return {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_api}"
}

headers = get_headers()

def search_movie(query: str):
    url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
    params = {
        'query': query,
        'include_adult': True,
        'language': 'en-US',
        'page': 1,
    }
    response = requests.get(url=url, headers=headers, params=params)
    return response.json()

def movie_details(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'language': 'en-US',
    }
    response = requests.get(url=url, headers=headers, params=params)
    return response.json()