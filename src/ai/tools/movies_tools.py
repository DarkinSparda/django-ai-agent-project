from tmdb import client as tmdb_client
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

@tool
def search_movies(query: str, config: RunnableConfig, limit: int=5):
    """
    """
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    response = tmdb_client.search_movie(query=query)
    try: 
        total_results = response.get("total_results")
        if total_results > 25:
            total_results = limit = 10
    except:
        total_results = -1
    
    if total_results == 0:
        return []
    
    return response['results'][:limit]

@tool
def movie_details(id: int, config: RunnableConfig):
    """
    """
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    try:
        response = tmdb_client.movie_details(id)
    
    except:
        raise Exception("movie not found or doesnt exist")
    
    return response


movie_tools = [
    search_movies,
    movie_details
]