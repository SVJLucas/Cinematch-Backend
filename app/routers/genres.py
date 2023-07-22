from typing import List
from routers import auth
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from database.management_factory import database_management
from firebase_admin.exceptions import FirebaseError
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.genres import Genre, GenrePost, GenreUpdate, GenreDelete, GenreResponse

# todo: genres sanity check (ex: unique)

router = APIRouter()
management = database_management['genres']


@router.get('/genres/{genre_id}', response_model=GenreResponse, status_code=status.HTTP_200_OK)
async def get_genre(genre_id: str, db: Reference = Depends(get_database)) -> GenreResponse:
    """

    Retrieve a specific genre from the database by its ID.

    Parameters:
        genre_id (str): The ID of the genre to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        genre (GenreResponse): The genre data, retrieved from the database and modeled as a GenreResponse object.

    """
    # Get the data from the manager
    genre = management.get_by_id(id=genre_id,
                                 db=db)

    # Convert the dictionary to a GenreResponse object
    genre = GenreResponse(**genre)

    return genre


@router.get('/genres', response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def get_genres(db: Reference = Depends(get_database)):
    """

    Retrieve all genres from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        genres (List[GenreResponse]): A list of genre data, retrieved from the database.

    """
    # Get the data from the manager
    genres = management.get_all(db=db)

    # Convert each dictionary in genres_data to a GenreResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    genres = list(GenreResponse(**genre) for genre in genres)

    return genres


@router.get('/genres/by_movie/{movie_id}', response_model=List[GenreResponse], status_code=status.HTTP_200_OK)
async def get_genres_by_movie(movie_id: str, db: Reference = Depends(get_database)):
    """

    Retrieve all movies_genres from the database.

    Parameters:
        movie_id: ID of the movie corresponding to the desired genres
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movies_genres (List[MovieGenreResponse]): A list of movie_genre data, retrieved from the database.

    """
    # Get the data from the manager
    movies_genres = database_management['movies_genres']

    # Get the genre ids for the desired movie
    filtered_movies_genres = movies_genres.get_by_field(field="movie_id", value=movie_id, db=db)
    genres_ids = [movie_genre["genre_id"] for movie_genre in filtered_movies_genres]

    # Get the genre data
    genres = [management.get_by_id(genre_id, db=db) for genre_id in genres_ids]

    # Convert each dictionary in movies_genres_data to a MovieGenreResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    movies_genres = list(GenreResponse(**genre) for genre in genres)

    return movies_genres

@router.post('/genres', status_code=status.HTTP_201_CREATED, response_model=GenreResponse)
async def post_genre(genre: GenrePost, db: Reference = Depends(get_database),
                     current_admin_id: str = Depends(auth.get_current_admin)):
    """
    Create a new genre in the database.

    Parameters:
        genre (GenrePost): The genre data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_admin_id (str): The ID of the admin to authenticate.

    Returns:
        genre (GenrePost): The created genre data, retrieved from the database.

    """

    # Converting the data to a dict, ready for Firebase
    genre = genre.dict()

    value = genre['name']

    # Check if the genre already exists
    if management.get_by_field(field='name', value=value, db=db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Genre already registered.')

    # Get the data from the manager
    genre = management.post(obj_data=genre,
                            db=db)
    # Return the created genre data, along with a 201 status code
    return GenreResponse(**genre)


@router.delete('/genres/{genre_id}', response_model=GenreResponse, status_code=status.HTTP_200_OK)
async def delete_genre(genre_id: str, db: Reference = Depends(get_database),
                       current_admin_id: str = Depends(auth.get_current_admin)) -> GenreResponse:
    """

    Deletes the genre from database given it's ID

    Parameters:
        genre_id (str): The ID of the genre to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_admin_id (str): The ID of the admin to authenticate.

    Returns:
        genre (GenreResponse): The genre data, deleted from the database and modeled as a GenreResponse object.

    """
    # Delete the data from the manager and return it
    genre = management.delete(id=genre_id,
                              db=db)

    # Convert the dictionary to a GenreResponse object
    genre = GenreResponse(**genre)

    return genre


@router.put('/genres/{genre_id}', status_code=status.HTTP_200_OK, response_model=GenreResponse)
async def put_genre(genre_id: str, genre: GenreUpdate, db: Reference = Depends(get_database),
                    current_admin_id: str = Depends(auth.get_current_admin)) -> GenreResponse:
    """
    Updates a genre in the database.

    Parameters:
        genre_id (str): The ID of the genre to retrieve.
        genre (GenreUpdate): The genre data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_admin_id (str): The ID of the admin to authenticate.

    Returns:
        genre (GenreResponse): The updated genre data, retrieved from the database.
    """
    # Convert the GenreUpdate Pydantic model to a dict
    genre = genre.dict()

    # Delete the data from the manager and return it
    updated_genre = management.update(id=genre_id,
                                      obj_data=genre,
                                      db=db)

    # Convert the dict to a GenreResponse Pydantic model and return it
    return GenreResponse(**updated_genre)
