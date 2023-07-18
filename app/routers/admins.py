from typing import List
from utils.hashing import Hashing
from firebase_admin.db import Reference
from database.database import get_database
from database.management import DatabaseManagement
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.admins import Admin, AdminPost, AdminUpdate, AdminDelete, AdminResponse

router = APIRouter()

hashing = Hashing()

management = DatabaseManagement(table_name='Admins',
                                class_name_id='admin_id')


@router.get('/admins/{admin_id}', response_model=AdminResponse, status_code=status.HTTP_200_OK)
async def get_admin(admin_id: str, db: Reference = Depends(get_database)) -> AdminResponse:
    """
    Retrieve a specific admin from the database by their ID.

    Parameters:
        admin_id (str): The ID of the admin to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        admin (AdminResponse): The admin data, retrieved from the database and modeled as a AdminResponse object.
    """
    # Get the data from the manager
    admin = management.get_by_id(id=admin_id, db=db)

    # Convert the dictionary to a AdminResponse object
    admin = AdminResponse(**admin)

    return admin


@router.get('/admins', response_model=List[AdminResponse], status_code=status.HTTP_200_OK)
async def get_admins(db: Reference = Depends(get_database)):
    """
    Retrieve all admins from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        admins (List[AdminResponse]): A list of admin data, retrieved from the database.
    """
    # Get the data from the manager
    admins = management.get_all(db=db)

    # Convert each dictionary in admins_data to a AdminResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    admins = list(AdminResponse(**admin) for admin in admins)

    return admins


@router.post('/admins', status_code=status.HTTP_201_CREATED, response_model=AdminResponse)
async def post_admin(admin: AdminPost, db: Reference = Depends(get_database)):

    """

    Create a new admin in the database.

    Parameters:
        admin (AdminPost): The admin data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        admin (AdminResponse): The created admin data, retrieved from the database.

    """

    # Convert the admin data to a dict, ready for Firebase
    admin_data = admin.dict()

    # Hashing password before it enter the database
    admin_data['password'] = hashing.hash_password(admin_data['password'])

    # Get the data from the manager
    admin_data = management.post(obj_data=admin_data, db=db)

    # Return the created admin data, along with a 201 status code
    return AdminResponse(**admin_data)


@router.delete('/admins/{admin_id}', response_model=AdminResponse, status_code=status.HTTP_200_OK)
async def delete_admin(admin_id: str, db: Reference = Depends(get_database)) -> AdminResponse:
    """
    Deletes the admin from the database given their ID.

    Parameters:
        admin_id (str): The ID of the admin to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        admin (AdminResponse): The admin data, deleted from the database and modeled as a AdminResponse object.
    """
    # Delete the data from the manager and return it
    admin_data = management.delete(id=admin_id, db=db)

    # Convert the dictionary to a AdminResponse object
    admin_data = AdminResponse(**admin_data)

    return admin_data


@router.put('/admins/{admin_id}', status_code=status.HTTP_200_OK, response_model=AdminResponse)
async def put_admin(admin_id: str, admin: AdminUpdate, db: Reference = Depends(get_database)) -> AdminResponse:
    """
    Updates a admin in the database.

    Parameters:
        admin_id (str): The ID of the admin to retrieve.
        admin (AdminUpdate): The admin data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        admin (AdminResponse): The updated admin data, retrieved from the database.
    """
    # Convert the AdminUpdate Pydantic model to a dict
    admin_data = admin.dict()

    # Check if the admin exists by ID
    if not management.get_by_id(id=admin_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Admin not found.")

    # Update the admin data in the manager and return the updated data
    updated_admin_data = management.update(id=admin_id, obj_data=admin_data, db=db)

    # Convert the dict to a AdminResponse Pydantic model and return it
    return AdminResponse(**updated_admin_data)
