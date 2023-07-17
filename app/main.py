from fastapi import FastAPI
from routers import genres, movies, movies_genres
from database.database import connect_to_database
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the FastAPI application
app = FastAPI(title='CinematchAPI')

# Connect to the Firebase database
connect_to_database()

# Include routers, assigning tags to categorize the routes in the API docs
# The genre-related routes
app.include_router(genres.router,tags=['Genres'])
# The movie-related routes
app.include_router(movies.router,tags=['Movies'])
# The routes related to relationships between movies and genres
app.include_router(movies_genres.router,tags=['Movies and Genres Relations'])
