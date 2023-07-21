from routers import auth
from typing import List
from utils.constants import *
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from database.management_factory import database_management
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.ratings import Rating, RatingPost, RatingResponse, RatingUpdate

router = APIRouter()
management = database_management['ratings']


def rating_sanity_check(rating_data: dict, db: Reference):
    users = database_management['users']
    movies = database_management['movies']

    # Verify if the user_id and movie_id exist in the corresponding collections
    user_id = rating_data['user_id']
    movie_id = rating_data['movie_id']

    if not users.get_by_id(id=user_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if not movies.get_by_id(id=movie_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    min_rating = MIN_RATING
    max_rating = MAX_RATING
    score = rating_data['score']
    if not min_rating <= score <= max_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid rating score. Score must be between 0 and 5.")


@router.get('/ratings/{rating_id}', response_model=RatingResponse, status_code=status.HTTP_200_OK)
async def get_rating(rating_id: str, db: Reference = Depends(get_database)) -> RatingResponse:
    """
        Retrieve a specific rating from the database by its ID.

        Parameters:
            rating_id (str): The ID of the rating to retrieve.
            db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

        Returns:
            rating (RatingResponse): The rating data, retrieved from the database and modeled as a RatingResponse object.
        """
    # Get the data from the manager
    rating = management.get_by_id(id=rating_id, db=db)

    # Convert the dictionary to a RatingResponse object
    rating = RatingResponse(**rating)

    return rating


@router.get('/ratings', response_model=List[RatingResponse], status_code=status.HTTP_200_OK)
async def get_ratings(db: Reference = Depends(get_database)):
    """
        Retrieve all ratings from the database.

        Parameters:
            db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

        Returns:
            ratings (List[RatingResponse]): A list of rating data, retrieved from the database.
        """
    # Get the data from the manager
    ratings = management.get_all(db=db)

    # Convert each dictionary in ratings_data to a RatingResponse object
    ratings = list(RatingResponse(**rating) for rating in ratings)

    return ratings


@router.post('/ratings', status_code=status.HTTP_201_CREATED, response_model=RatingResponse)
async def post_rating(rating: RatingPost, db: Reference = Depends(get_database),
                      current_user_id: str = Depends(auth.get_current_user)):
    """
    Create a new rating in the database.

    Parameters:
        rating (RatingPost): The rating data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_user_id (str): The ID of the user to retrieve

    Returns:
        rating (RatingResponse): The created rating data, retrieved from the database.
    """
    # Convert the rating data to a dict, ready for Firebase
    rating_data = rating.dict()

    # Add the user_id to rating data
    rating_data['user_id'] = current_user_id

    # Verify if user has already rated the movie
    user_ratings = management.get_by_field(field='user_id', value=current_user_id, db=db)
    existing_rating = any([user_rating['movie_id'] == rating_data['movie_id'] for user_rating in user_ratings])
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user has already rated this movie.")

    # Perform sanity checks for the rating data
    rating_sanity_check(rating_data, db)

    # Get the data from the manager
    rating_data = management.post(obj_data=rating_data, db=db)

    # Return the created rating data, along with a 201 status code
    return RatingResponse(**rating_data)


@router.delete('/ratings/{rating_id}', response_model=RatingResponse, status_code=status.HTTP_200_OK)
async def delete_rating(rating_id: str, db: Reference = Depends(get_database),
                        current_user_id: str = Depends(auth.get_current_user)) -> RatingResponse:
    """
    Deletes the rating from the database given its ID.

    Parameters:
        rating_id (str): The ID of the rating to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_user_id (str): The ID of the user to retrieve

    Returns:
        rating (RatingResponse): The rating data, deleted from the database and modeled as a RatingResponse object.
    """
    # Verify if the user has authorization to delete the rating
    old_rating_data = management.get_by_id(id=rating_id, db=db)
    if old_rating_data['user_id'] != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The user doesn't have authorization to delete this rating")

    # Delete the data from the manager and return it
    rating_data = management.delete(id=rating_id, db=db)

    # Convert the dictionary to a RatingResponse object
    rating_data = RatingResponse(**rating_data)

    return rating_data


@router.put('/ratings/{rating_id}', status_code=status.HTTP_200_OK, response_model=RatingResponse)
async def put_rating(rating_id: str, rating: RatingUpdate, db: Reference = Depends(get_database),
                     current_user_id: str = Depends(auth.get_current_user)) -> RatingResponse:
    """
    Updates a rating in the database.

    Parameters:
        rating_id (str): The ID of the rating to retrieve.
        rating (RatingUpdate): The rating data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.
        current_user_id (str): The ID of the user to retrieve

    Returns:
        rating (RatingResponse): The updated rating data, retrieved from the database.
    """
    # Convert the RatingUpdate Pydantic model to a dict
    rating_data = rating.dict()

    # Get the old rating data
    old_rating_data = management.get_by_id(id=rating_id, db=db)

    # Add the user_id and movie_id to rating data
    rating_data['user_id'] = current_user_id
    rating_data['movie_id'] = old_rating_data['movie_id']

    # Check if the rating exists by ID
    if not management.get_by_id(id=rating_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found.")

    # Perform sanity checks for the rating data
    rating_sanity_check(rating_data, db)

    # Verify if the user has authorization to modify the rating
    if old_rating_data['user_id'] != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The user doesn't have authorization to modify this rating")

    # Update the rating data in the manager and return the updated data
    updated_rating_data = management.update(id=rating_id, obj_data=rating_data, db=db)

    # Convert the dict to a RatingResponse Pydantic model and return it
    return RatingResponse(**updated_rating_data)
