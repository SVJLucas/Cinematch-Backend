from typing import List
from firebase_admin.db import Reference
from database.database import get_database
from database.management import DatabaseManagement
from fastapi import APIRouter, status, Depends, HTTPException
from routers import movies, genres
from schemas.movies_genres import MovieGenre, MovieGenrePost, MovieGenreUpdate, MovieGenreDelete, MovieGenreResponse


from utils.constants import *

router = APIRouter()
management = DatabaseManagement(table_name='MoviesGenres',
                                class_name_id='movie_genre_id')


def movie_genre_sanity_check(movie_genre: dict, db: Reference):
    movie_id = movie_genre['movie_id']
    genre_id = movie_genre['genre_id']

    if not movies.management.verify_id(id=movie_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    if not genres.management.verify_id(id=genre_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found.")


@router.get('/moviesgenres/{movie_genre_id}', response_model=MovieGenreResponse, status_code=status.HTTP_200_OK)
async def get_movie_genre(movie_genre_id: str, db: Reference = Depends(get_database)) -> MovieGenreResponse:
    """

    Retrieve a specific movie_genre from the database by its ID.

    Parameters:
        movie_genre_id (str): The ID of the movie_genre to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie_genre (MovieGenreResponse): The movie_genre data, retrieved from the database and modeled as a MovieGenreResponse object.

    """
    # Get the data from the manager
    movie_genre = management.get_by_id(id=movie_genre_id,
                                       db=db)

    # Convert the dictionary to a MovieGenreResponse object
    movie_genre = MovieGenreResponse(**movie_genre)

    return movie_genre


@router.get('/moviesgenres', response_model=List[MovieGenreResponse], status_code=status.HTTP_200_OK)
async def get_movies_genres(db: Reference = Depends(get_database)):
    """

    Retrieve all movies_genres from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movies_genres (List[MovieGenreResponse]): A list of movie_genre data, retrieved from the database.

    """
    # Get the data from the manager
    movies_genres = management.get_all(db=db)

    # Convert each dictionary in movies_genres_data to a MovieGenreResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    movies_genres = list(MovieGenreResponse(**movie_genre) for movie_genre in movies_genres)

    return movies_genres


@router.post('/moviesgenres', status_code=status.HTTP_201_CREATED, response_model=MovieGenreResponse)
async def post_movie_genre(movie_genre: MovieGenrePost, db: Reference = Depends(get_database)):
    """
    Create a new movie_genre in the database.

    Parameters:
        movie_genre (MovieGenrePost): The movie_genre data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie_genre (MovieGenrePost): The created movie_genre data, retrieved from the database.

    """
    # Convert the movie_genre data to a dict, ready for Firebase
    movie_genre = movie_genre.dict()

    # Do the movie genre check
    movie_genre_sanity_check(movie_genre, db)

    # Get the data from the manager
    movie_genre = management.post(obj_data=movie_genre,
                                  db=db)

    # Return the created movie_genre data, along with a 201 status code
    return MovieGenreResponse(**movie_genre)


@router.delete('/moviesgenres/{movie_genre_id}', response_model=MovieGenreResponse, status_code=status.HTTP_200_OK)
async def delete_movie_genre(movie_genre_id: str, db: Reference = Depends(get_database)) -> MovieGenreResponse:
    """

    Deletes the movie_genre from database given it's ID

    Parameters:
        movie_genre_id (str): The ID of the movie_genre to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie_genre (MovieGenreResponse): The movie_genre data, deleted from the database and modeled as a MovieGenreResponse object.

    """
    # Delete the data from the manager and return it
    movie_genre = management.delete(id=movie_genre_id,
                                    db=db)

    # Convert the dictionary to a MovieGenreResponse object
    movie_genre = MovieGenreResponse(**movie_genre)

    return movie_genre


@router.put('/moviesgenres/{movie_genre_id}', status_code=status.HTTP_200_OK, response_model=MovieGenreResponse)
async def put_movie_genre(movie_genre_id: str, movie_genre: MovieGenreUpdate,
                          db: Reference = Depends(get_database)) -> MovieGenreResponse:
    """
    Updates a movie_genre in the database.

    Parameters:
        movie_genre_id (str): The ID of the movie_genre to retrieve.
        movie_genre (MovieGenreUpdate): The movie_genre data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie_genre (MovieGenreResponse): The updated movie_genre data, retrieved from the database.
    """
    # Convert the GenreUpdate Pydantic model to a dict
    movie_genre = movie_genre.dict()

    # Do the movie genre check
    movie_genre_sanity_check(movie_genre, db)

    # Delete the data from the manager and return it
    updated_movie_genre = management.update(id=movie_genre_id,
                                            obj_data=movie_genre,
                                            db=db)

    # Convert the dict to a MovieGenreResponse Pydantic model and return it
    return MovieGenreResponse(**updated_movie_genre)
