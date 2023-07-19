from typing import List
from utils.constants import *
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from database.management_factory import database_management
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.recommendations import Recommendation, RecommendationPost, RecommendationResponse, RecommendationUpdate

router = APIRouter()
management = database_management['recommendations']


def recommendation_sanity_check(rec_data: dict, db: Reference):
    users = database_management['users']
    movies = database_management['movies']

    # Verify if the user_id and movie_id exist in the corresponding collections
    user_id = rec_data['user_id']
    movie_id = rec_data['movie_id']

    if not users.management.verify_id(id=user_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if not movies.management.verify_id(id=movie_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")


@router.get('/recommendations/{recommendation_id}', response_model=RecommendationResponse, status_code=status.HTTP_200_OK)
async def get_recommendation(recommendation_id: str, db: Reference = Depends(get_database),) -> RecommendationResponse:
    """
        Retrieve a specific recommendation from the database by its ID.

        Parameters:
            recommendation_id (str): The ID of the recommendation to retrieve.
            db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

        Returns:
            recommendation (RecommendationResponse): The recommendation data, retrieved from the database and modeled as a RecommendationResponse object.
        """
    # Get the data from the manager
    recommendation = management.get_by_id(id=recommendation_id, db=db)

    # Convert the dictionary to a RecommendationResponse object
    recommendation = RecommendationResponse(**recommendation)

    return recommendation


@router.get('/recommendations', response_model=List[RecommendationResponse], status_code=status.HTTP_200_OK)
async def get_recommendations(db: Reference = Depends(get_database)):
    """
    Retrieve all recommendations from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        recommendations (List[RecommendationResponse]): A list of recommendation data, retrieved from the database.
    """
    # Get the data from the manager
    recommendations = management.get_all(db=db)

    # Convert each dictionary in recommendations_data to a RecommendationResponse object
    recommendations = list(RecommendationResponse(**recommendation) for recommendation in recommendations)

    return recommendations


@router.post('/recommendations', status_code=status.HTTP_201_CREATED, response_model=RecommendationResponse)
async def post_recommendation(recommendation: RecommendationPost, db: Reference = Depends(get_database)):
    """
    Create a new recommendation in the database.

    Parameters:
        recommendation (RecommendationPost): The recommendation data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        recommendation (RecommendationResponse): The created recommendation data, retrieved from the database.
    """
    # Convert the recommendation data to a dict, ready for Firebase
    rec_data = recommendation.dict()

    # Perform sanity checks for the recommendation data
    recommendation_sanity_check(rec_data, db)

    # Get the data from the manager
    rec_data = management.post(obj_data=rec_data, db=db)

    # Return the created recommendation data, along with a 201 status code
    return RecommendationResponse(**rec_data)


@router.delete('/recommendations/{recommendation_id}', response_model=RecommendationResponse, status_code=status.HTTP_200_OK)
async def delete_recommendation(recommendation_id: str, db: Reference = Depends(get_database)) -> RecommendationResponse:
    """
        Deletes the recommendation from the database given its ID.

        Parameters:
            recommendation_id (str): The ID of the recommendation to retrieve.
            db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

        Returns:
            recommendation (RecommendationResponse): The recommendation data, deleted from the database and modeled as a RecommendationResponse object.
        """
    # Delete the data from the manager and return it
    recommendation_data = management.delete(id=recommendation_id, db=db)

    # Convert the dictionary to a RecommendationResponse object
    recommendation_data = RecommendationResponse(**recommendation_data)

    return recommendation_data


@router.put('/recommendations/{recommendation_id}', status_code=status.HTTP_200_OK, response_model=RecommendationResponse)
async def put_recommendation(recommendation_id: str, recommendation: RecommendationUpdate, db: Reference = Depends(get_database)) -> RecommendationResponse:
    """
    Updates a recommendation in the database.

    Parameters:
        recommendation_id (str): The ID of the recommendation to retrieve.
        recommendation (RecommendationUpdate): The recommendation data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        recommendation (RecommendationResponse): The updated recommendation data, retrieved from the database.
    """
    # Convert the RecommendationUpdate Pydantic model to a dict
    rec_data = recommendation.dict()

    # Check if the recommendation exists by ID
    if not management.get_by_id(id=recommendation_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found.")

    # Perform sanity checks for the recommendation data
    recommendation_sanity_check(rec_data, db)

    # Update the recommendation data in the manager and return the updated data
    updated_rec_data = management.update(id=recommendation_id, obj_data=rec_data, db=db)

    # Convert the dict to a RecommendationResponse Pydantic model and return it
    return RecommendationResponse(**updated_rec_data)

