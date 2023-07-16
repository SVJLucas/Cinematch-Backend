import os
import firebase_admin
from firebase_admin import db


def connect_to_database():
    """
    Function to connect to a Firebase real-time database.

    It reads the path to Firebase credential and the database URL from environment variables.
    Then it initializes the Firebase application with these credentials and URL.
    Finally, it returns a database reference to the root of the database.

    Returns:
    db.Reference: A reference to the root of the Firebase database.
    """
    # Get the path to Firebase credentials from environment variables
    path_to_certificate = os.getenv('PATH_TO_CREDENTIALS')
    # Get the Firebase database URL from environment variables
    database_URL = os.getenv('DATABASE_URL')
    # Initialize a credential object using the Firebase certificate at the path we obtained earlier
    cred_object = firebase_admin.credentials.Certificate(path_to_certificate)
    # Initialize the Firebase app with the credential object and the database URL
    default_app = firebase_admin.initialize_app(cred_object, {
        'databaseURL': database_URL
    })
    # Return a reference to the root of the database
    return db.reference('/')



