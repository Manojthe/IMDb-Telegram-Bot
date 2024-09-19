from imdb import IMDb

# Initialize IMDb instance
ia = IMDb()

def search_movies(query):
    """Search movies by query."""
    return ia.search_movie(query)

def fetch_movie_details(movie_id):
    """Fetch details for a particular movie."""
    movie = ia.get_movie(movie_id)

    title = movie.get('title', 'N/A')
    rating = movie.get('rating', 'N/A')
    year = movie.get('year', 'N/A')
    duration = movie.get('runtime', ['N/A'])[0] if movie.get('runtime') else 'N/A'
    languages = ', '.join(movie.get('languages', ['N/A']))
    genres = ', '.join(movie.get('genres', ['N/A']))
    plot = movie.get('plot outline', 'N/A')
    directors = ', '.join([director.get('name', 'N/A') for director in movie.get('directors', [])])
    actors = ', '.join([actor.get('name', 'N/A') for actor in movie.get('cast', [])[:5]])
    writers = ', '.join([writer.get('name', 'N/A') for writer in movie.get('writers', [])])
    poster_url = movie.get('full-size cover url', '')

    return {
        'title': title,
        'rating': rating,
        'year': year,
        'duration': duration,
        'languages': languages,
        'genres': genres,
        'plot': plot,
        'directors': directors,
        'actors': actors,
        'writers': writers,
        'poster_url': poster_url
    }
