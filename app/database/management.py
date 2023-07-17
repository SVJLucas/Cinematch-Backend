from typing import List
from datetime import datetime
from firebase_admin.db import Reference
from database.database import get_database
from firebase_admin.exceptions import FirebaseError
from fastapi import APIRouter, status, Depends, HTTPException


# noinspection PyTypeChecker,PyUnresolvedReferences
class DatabaseManagement:
    def __init__(self, table_name: str, class_name_id: str):
        self.table_name = table_name
        self.class_name_id = class_name_id

    def get_by_id(self, id: str, db: Reference) -> dict:
        """
            Retrieve a specific object from the database by its ID.

            Parameters:
                id (str): The ID of the object to retrieve.
                class_name_id (str): Name of the attribute id (ex: 'movie_id', 'genre_id')
                table_name (str): Name of the table to look at
                db (Reference): A reference to the Firebase database, injected by FastAPI's dependency injection.

            Returns:
                response (dict): The object data, retrieved from the database as a dictionary object.

            """
        try:
            # Construct a reference to the specific genre in Firebase
            reference = db.child(self.table_name).child(id)

            # Use the reference to get the genre data
            response = reference.get()
        except FirebaseError as error:
            # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while trying to fetch data: {error}")

        # If the response data is None, that means the response was not found
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{self.class_name_id} == {id} was not found.")

        # If the response data is not None, we add the id to the dictionary
        else:
            response[self.class_name_id] = id

        return response

    def get_all(self, db: Reference) -> List[dict]:
        try:
            # Get all objects from Firebase
            objects = db.child(self.table_name).get()
        except FirebaseError as error:
            # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while trying to fetch data: {error}")

            # Create a list of dictionaries, adding the key as 'id' to each dictionary
            # Here, key is the unique id generated by Firebase, and value is the corresponding object data
        objects_data = [{self.class_name_id: key, **value} for key, value in objects.items() if value]

        return objects_data

    def post(self, obj_data: dict, db: Reference) -> dict:

        # Create the 'created_at' field with reference in UTC time
        obj_data['created_at'] = datetime.utcnow().isoformat()

        try:
            # Create a new reference in the table, with a unique key
            reference = db.child(self.table_name).push()

            # Set the object data at the new reference
            reference.set(obj_data)

            # Retrieve the created object data using the new reference
            # We do this to include any server-side transformations or additions (like the created time) in the response
            obj_data = reference.get()

            # Adding the primary key
            obj_data[self.class_name_id] = reference.key

            # Return the created object data, along with a 201 status code
            return obj_data

        except FirebaseError as error:
            # If an error occurred while interacting with Firebase, return a 500 status code with a helpful message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while trying to push data: {error}")

    def delete(self, id: str, db: Reference) -> dict:
        try:
            # Construct a reference to the specific object in Firebase
            reference = db.child(self.table_name).child(id)

            # Use the reference to get the object data
            obj_data = reference.get()

            if obj_data is not None:
                # Deleting the desired data
                reference.delete()
                # If the object data is not None, we add the id to the dictionary
                obj_data[self.class_name_id] = id
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"{self.class_name_id} == {id} was not found.")

            return obj_data

        except FirebaseError as error:
            # If an error occurred while interacting with Firebase, raise a 500 status code with a helpful message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while trying to fetch data: {error}")

    def update(self, id: str, obj_data: dict, db: Reference) -> dict:
        try:
            # Create a reference to the object in the table in Firebase
            reference = db.child(self.table_name).child(id)

            # Get the current object data
            old_obj_data = reference.get()

            # If the object doesn't exist, raise a 404 Not Found exception
            if old_obj_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"{self.class_name_id} == {id} was not found.")

            # If the object exists, keep the created_at timestamp unchanged
            obj_data['created_at'] = old_obj_data['created_at']

            # Update the object data at the reference
            reference.update(obj_data)

            # Retrieve the updated object data from Firebase
            # This includes any server-side transformations or additions
            updated_obj_data = reference.get()

            # Add the id to the object data
            updated_obj_data[self.class_name_id] = id

            return updated_obj_data

        except FirebaseError as error:
            # If an error occurred while interacting with Firebase, raise a 500 Internal Server Error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while trying to update the object: {error}")
