from routers import auth
from typing import List
from utils.hashing import Hashing
from firebase_admin.db import Reference
from database.database import get_database
from database.management_factory import database_management
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.ais import Ai, AiPost, AiUpdate, AiDelete, AiResponse

router = APIRouter()

hashing = Hashing()

management = database_management['ais']


@router.get('/ais/{ai_id}', response_model=AiResponse, status_code=status.HTTP_200_OK)
async def get_ai(ai_id: str, db: Reference = Depends(get_database),
                 current_admin_id: str = Depends(auth.get_current_admin)) -> AiResponse:
    """
    Retrieve a specific ai from the database by their ID.

    Parameters:
        ai_id (str): The ID of the ai to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        ai (AiResponse): The ai data, retrieved from the database and modeled as a AiResponse object.
    """
    # Get the data from the manager
    ai = management.get_by_id(id=ai_id, db=db)

    # Convert the dictionary to a AiResponse object
    ai = AiResponse(**ai)

    return ai


@router.get('/ais', response_model=List[AiResponse], status_code=status.HTTP_200_OK)
async def get_ais(db: Reference = Depends(get_database),
                  current_admin_id: str = Depends(auth.get_current_admin)):
    """
    Retrieve all ais from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        ais (List[AiResponse]): A list of ai data, retrieved from the database.
    """
    # Get the data from the manager
    ais = management.get_all(db=db)

    # Convert each dictionary in ais_data to a AiResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    ais = list(AiResponse(**ai) for ai in ais)

    return ais


@router.post('/ais', status_code=status.HTTP_201_CREATED, response_model=AiResponse)
async def post_ai(ai: AiPost, db: Reference = Depends(get_database),
                  current_admin_id: str = Depends(auth.get_current_admin)):
    """
    Create a new ai in the database.

    Parameters:
        ai (AiPost): The ai data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        ai (AiResponse): The created ai data, retrieved from the database.

    """
    # Convert the ai data to a dict, ready for Firebase
    ai_data = ai.dict()

    # Hashing password before it enter the database
    ai_data['password'] = hashing.hash_password(ai_data['password'])

    # Get the data from the manager
    ai_data = management.post(obj_data=ai_data, db=db)

    # Return the created ai data, along with a 201 status code
    return AiResponse(**ai_data)


@router.delete('/ais/{ai_id}', response_model=AiResponse, status_code=status.HTTP_200_OK)
async def delete_ai(ai_id: str, db: Reference = Depends(get_database),current_admin_id: str = Depends(auth.get_current_admin)) -> AiResponse:
    """
    Deletes the ai from the database given their ID.

    Parameters:
        ai_id (str): The ID of the ai to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        ai (AiResponse): The ai data, deleted from the database and modeled as a AiResponse object.
    """
    # Delete the data from the manager and return it
    ai_data = management.delete(id=ai_id, db=db)

    # Convert the dictionary to a AiResponse object
    ai_data = AiResponse(**ai_data)

    return ai_data


@router.put('/ais/{ai_id}', status_code=status.HTTP_200_OK, response_model=AiResponse)
async def put_ai(ai_id: str, ai: AiUpdate, db: Reference = Depends(get_database),
                 current_admin_id: str = Depends(auth.get_current_admin)) -> AiResponse:
    """
    Updates a ai in the database.

    Parameters:
        ai_id (str): The ID of the ai to retrieve.
        ai (AiUpdate): The ai data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        ai (AiResponse): The updated ai data, retrieved from the database.
    """
    # Convert the AiUpdate Pydantic model to a dict
    ai_data = ai.dict()

    # Check if the ai exists by ID
    if not management.get_by_id(id=ai_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ai not found.")

    # Update the ai data in the manager and return the updated data
    updated_ai_data = management.update(id=ai_id, obj_data=ai_data, db=db)

    # Convert the dict to a AiResponse Pydantic model and return it
    return AiResponse(**updated_ai_data)
