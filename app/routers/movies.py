from typing import List
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from firebase_admin.exceptions import FirebaseError
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.movies import Movie, MoviePost, MovieUpdate, MovieDelete, MovieResponse

router = APIRouter()


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
    try:
        # Construct a reference to the specific movie in Firebase
        reference = db.child('Movies').child(movie_id)

        # Use the reference to get the movie data
        movie = reference.get()
    except FirebaseError as error:
        # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while trying to fetch data: {error}")

    # If the movie data is None, that means the movie was not found
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Movie ID {movie_id} was not found.")

    # If the movie data is not None, we add the movie_id to the dictionary
    else:
        movie['movie_id'] = movie_id

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

    try:
        # Get all movies from Firebase
        movies = db.child('Movies').get()
    except FirebaseError as error:
        # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while trying to fetch data: {error}")

    # Create a list of dictionaries, adding the key as 'movie_id' to each dictionary
    # Here, key is the unique id generated by Firebase, and value is the corresponding movie data
    movies = [{'movie_id': key, **value} for key, value in movies.items() if value]

    # Convert each dictionary in movies_data to a MovieResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    movies = list(MovieResponse(**movie) for movie in movies)

    return movies


@router.post('/movies', status_code=status.HTTP_201_CREATED, response_model=MovieResponse)
async def post_movie(movie: MoviePost, db: Reference = Depends(get_database)):
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

    # Create the 'created_at' field with reference in UTC time
    movie['created_at'] = datetime.utcnow().isoformat()

    try:
        # Create a new reference in the 'Movies' node, with a unique key
        reference = db.child('Movies').push()

        # Set the movie data at the new reference
        reference.set(movie)

        # Retrieve the created movie data using the new reference
        # We do this to include any server-side transformations or additions (like the created time) in the response
        movie = reference.get()

        # Adding the primary key
        movie['movie_id'] = reference.key

        # Return the created movie data, along with a 201 status code
        return MovieResponse(**movie)

    except FirebaseError as error:
        # If an error occurred while interacting with Firebase, return a 500 status code with a helpful message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while trying to push data: {error}")


@router.delete('/movies/{movie_id}', response_model=MovieResponse, status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: str, db: Reference = Depends(get_database)) -> MovieResponse:

    """

    Deletes the movie from database given it's ID

    Parameters:
        movie_id (str): The ID of the movie to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MovieResponse): The movie data, deleted from the database and modeled as a MovieResponse object.

    """
    try:
        # Construct a reference to the specific movie in Firebase
        reference = db.child('Movies').child(movie_id)

        # Use the reference to get the movie data
        movie = reference.get()

        if movie is not None:
            # Deleting the desired data
            reference.delete()

    except FirebaseError as error:
        # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while trying to fetch data: {error}")

    # If the movie data is None, that means the movie was not found
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Movie ID {movie_id} was not found.")

    # If the movie data is not None, we add the movie_id to the dictionary
    else:
        movie['movie_id'] = movie_id

    # Convert the dictionary to a MovieResponse object
    movie = MovieResponse(**movie)

    return movie


@router.put('/movies', status_code=status.HTTP_200_OK, response_model=MovieResponse)
async def put_movie(movie: MovieUpdate, db: Reference = Depends(get_database)) -> MovieResponse:
    """
    Updates a movie in the database.

    Parameters:
        movie (MovieUpdate): The movie data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        movie (MovieResponse): The updated movie data, retrieved from the database.
    """

    # Convert the MovieUpdate Pydantic model to a dict
    movie = movie.dict()

    # Extract movie_id from the data and remove it from the dict
    movie_id = movie.pop('movie_id')

    try:
        # Create a reference to the movie in the 'Movies' node in Firebase
        reference = db.child('Movies').child(movie_id)

        # Get the current movie data
        old_movie = reference.get()

        # If the movie doesn't exist, raise a 404 Not Found exception
        if old_movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Movie ID {movie_id} was not found.")

        # If the movie exists, keep the created_at timestamp unchanged
        movie['created_at'] = old_movie['created_at']

        # Update the movie data at the reference
        reference.update(movie)

        # Retrieve the updated movie data from Firebase
        # This includes any server-side transformations or additions
        updated_movie = reference.get()

        # Add the movie_id to the movie data
        updated_movie['movie_id'] = movie_id

        # Convert the dict to a MovieResponse Pydantic model and return it
        return MovieResponse(**updated_movie)

    except FirebaseError as error:
        # If an error occurred while interacting with Firebase, raise a 500 Internal Server Error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while trying to update the movie: {error}")
