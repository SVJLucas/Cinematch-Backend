from typing import List
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from database.management import DatabaseManagement
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.users import User, UserPost, UserUpdate, UserDelete, UserResponse

router = APIRouter()
management = DatabaseManagement(table_name='Users',
                                class_name_id='user_id')


def user_sanity_check(user_data: dict, db: Reference):
    # Check if the email already exists in the database
    email = user_data['email']
    if management.get_by_field(field='email', value=email, db=db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")


@router.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: Reference = Depends(get_database)) -> UserResponse:
    """
    Retrieve a specific user from the database by their ID.

    Parameters:
        user_id (str): The ID of the user to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        user (UserResponse): The user data, retrieved from the database and modeled as a UserResponse object.
    """
    # Get the data from the manager
    user = management.get_by_id(id=user_id, db=db)

    # Convert the dictionary to a UserResponse object
    user = UserResponse(**user)

    return user


@router.get('/users', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: Reference = Depends(get_database)):
    """
    Retrieve all users from the database.

    Parameters:
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        users (List[UserResponse]): A list of user data, retrieved from the database.
    """
    # Get the data from the manager
    users = management.get_all(db=db)

    # Convert each dictionary in users_data to a UserResponse object
    # We're using a generator expression here instead of a list comprehension for better performance
    # A generator expression doesn't construct the whole list in memory, it generates each item on-the-fly
    users = list(UserResponse(**user) for user in users)

    return users


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def post_user(user: UserPost, db: Reference = Depends(get_database)):
    """
    Create a new user in the database.

    Parameters:
        user (UserPost): The user data to be saved, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        user (UserResponse): The created user data, retrieved from the database.
    """
    # Convert the user data to a dict, ready for Firebase
    user_data = user.dict()

    # Perform sanity checks for the user data
    user_sanity_check(user_data, db)

    # Get the data from the manager
    user_data = management.post(obj_data=user_data, db=db)

    # Return the created user data, along with a 201 status code
    return UserResponse(**user_data)


@router.delete('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, db: Reference = Depends(get_database)) -> UserResponse:
    """
    Deletes the user from the database given their ID.

    Parameters:
        user_id (str): The ID of the user to retrieve.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        user (UserResponse): The user data, deleted from the database and modeled as a UserResponse object.
    """
    # Delete the data from the manager and return it
    user_data = management.delete(id=user_id, db=db)

    # Convert the dictionary to a UserResponse object
    user_data = UserResponse(**user_data)

    return user_data


@router.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def put_user(user_id: str, user: UserUpdate, db: Reference = Depends(get_database)) -> UserResponse:
    """
    Updates a user in the database.

    Parameters:
        user_id (str): The ID of the user to retrieve.
        user (UserUpdate): The user data to be updated, parsed from the request body.
        db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

    Returns:
        user (UserResponse): The updated user data, retrieved from the database.
    """
    # Convert the UserUpdate Pydantic model to a dict
    user_data = user.dict()

    # Check if the user exists by ID
    if not management.get_by_id(id=user_id, db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")

    # Perform sanity checks for the user data
    user_sanity_check(user_data, db)

    # Update the user data in the manager and return the updated data
    updated_user_data = management.update(id=user_id, obj_data=user_data, db=db)

    # Convert the dict to a UserResponse Pydantic model and return it
    return UserResponse(**updated_user_data)
