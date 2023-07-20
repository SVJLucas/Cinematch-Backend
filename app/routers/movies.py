from routers import auth
from typing import List
from utils.constants import *
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from database.management_factory import database_management
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.movies import Movie, MoviePost, MovieUpdate, MovieDelete, MovieResponse


router = APIRouter()
management = database_management['movies']
movies_genres = database_management['movies_genres']


def movie_sanity_check(movie: dict):

    """

    Check if the movie details, specifically the year and rating, fall within valid ranges.

    Parameters:
    movie (dict): A dictionary containing details of a movie.

    Raises:
    HTTPException: If the movie year is not within the range MIN_YEAR to current year,
    or if the movie rating is not within the range MIN_RATING to MAX_RATING.

    """

    # The minimum year of movie release allowed
    min_year = MIN_YEAR

    # The maximum year of movie release allowed is set as the current year
    max_year = datetime.now().year

    # Extracting the year of the movie from the dictionary
    year = movie['year']

    # Checking if the year is within the defined range
    if year < min_year or year > max_year:
        # Raise an exception with status 400 if year is out of bounds
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Year {year} is not within the allowed bounds [{min_year}, {max_year}]")

    # The minimum movie rating allowed
    min_rating = MIN_RATING

    # The maximum movie rating allowed
    max_rating = MAX_RATING

    # Extracting the rating of the movie from the dictionary
    rating = movie['rating']

    # Checking if the rating is within the defined range
    if not min_rating <= rating <= max_rating:
        # Raise an exception with status 400 if rating is out of bounds
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Mean rating {rating} is not within the allowed bounds [{min_rating}, {max_rating}]")


@router.get('/movies/{movie_id}', response_model=MovieResponse, status_code=status.HTTP_200_OK)
async def get_movie(movie_id: str, db: Reference = Depends(get_database)) -> MovieResponse:
    """

    Retrieve a specific movie from the database by its ID.

    Parameters:
        movie_id (str): The ID of the movie to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MovieResponse): The movie data, retrieved from the database and modeled as a MovieResponse object.

    """

    # Get the data from the manager
    movie = management.get_by_id(id=movie_id,
                                 db=db)

    # Convert the dictionary to a MovieResponse object
    movie = MovieResponse(**movie)

    return movie


@router.get('/movies', response_model=List[MovieResponse], status_code=status.HTTP_200_OK)
async def get_movies(db: Reference = Depends(get_database)):
    """

    Retrieve all movies from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movies (List[MovieResponse]): A list of movie data, retrieved from the database.

    """

    # Get the data from the manager
    movies = management.get_all(db=db)

    # Convert each dictionary in movies_data to a MovieResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    movies = list(MovieResponse(**movie) for movie in movies)

    return movies


@router.get('/movies/by_genre/{genre_id}', response_model=List[MovieResponse], status_code=status.HTTP_200_OK)
async def get_movies_by_genre(genre_id: str, db: Reference = Depends(get_database)):
    """

    Retrieve all movies from the database for a specific genre.

    Parameters:
        genre_id (str): The id of the requested genre
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movies (List[MovieResponse]): A list of movie data, retrieved from the database.

    """
    # Get the data from the manager
    movies_genres_list = movies_genres.get_by_field(field='genre_id', value=genre_id, db=db)


    # Convert each dictionary in movies_data to a MovieResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    movies = list(MovieResponse(**(management.get_by_id(movie_genre['movie_id'], db=db)))
                  for movie_genre in movies_genres_list)

    return movies


@router.post('/movies', status_code=status.HTTP_201_CREATED, response_model=MovieResponse)
async def post_movie(movie: MoviePost, db: Reference = Depends(get_database), current_admin_id: str = Depends(auth.get_current_admin)):

    """
    Create a new movie in the database.

    Parameters:
        movie (MoviePost): The movie data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MoviePost): The created movie data, retrieved from the database.

    """

    # Convert the movie data to a dict, ready for Firebase
    movie = movie.dict()

    # Do the movie sanity check
    movie_sanity_check(movie)

    # Get the data from the manager
    movie = management.post(obj_data=movie,
                            db=db)

    # Return the created movie data, along with a 201 status code
    return MovieResponse(**movie)


@router.delete('/movies/{movie_id}', response_model=MovieResponse, status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: str, db: Reference = Depends(get_database),current_admin_id: str = Depends(auth.get_current_admin)) -> MovieResponse:

    """

    Deletes the movie from database given it's ID

    Parameters:
        movie_id (str): The ID of the movie to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MovieResponse): The movie data, deleted from the database and modeled as a MovieResponse object.

    """

    # Delete the data from the manager and return it
    movie = management.delete(id=movie_id,
                              db=db)

    # Convert the dictionary to a MovieResponse object
    movie = MovieResponse(**movie)

    return movie


@router.put('/movies/{movie_id}', status_code=status.HTTP_200_OK, response_model=MovieResponse)
async def put_movie(movie_id:str, movie: MovieUpdate, db: Reference = Depends(get_database),current_admin_id: str = Depends(auth.get_current_admin)) -> MovieResponse:

    """

    Updates a movie in the database.

    Parameters:
        movie_id (str): The ID of the movie to retrieve.
        movie (MovieUpdate): The movie data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MovieResponse): The updated movie data, retrieved from the database.
    """

    # Convert the MovieUpdate Pydantic model to a dict
    movie = movie.dict()

    # Do the movie sanity check
    movie_sanity_check(movie)

    # Delete the data from the manager and return it
    updated_movie = management.update(id=movie_id,
                                      obj_data=movie,
                                      db=db)

    # Convert the dict to a MovieResponse Pydantic model and return it
    return MovieResponse(**updated_movie)

