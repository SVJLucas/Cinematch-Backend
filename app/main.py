from fastapi import FastAPI
from dotenv import load_dotenv
from database.database import connect_to_database
from routers import users, admins, ais, genres, movies, movies_genres, recommendations, ratings, auth

# Load environment variables from a .env file
load_dotenv()

# Initialize the FastAPI application
app = FastAPI(title='CinematchAPI')

# Connect to the Firebase database
connect_to_database()

# Include routers, assigning tags to categorize the routes in the API docs
# The user-related routes
app.include_router(users.router,tags=['Users'])
# The genre-related routes
app.include_router(genres.router,tags=['Genres'])
# The movie-related routes
app.include_router(movies.router,tags=['Movies'])
# The routes related to relationships between movies and genres
app.include_router(movies_genres.router,tags=['Movies and Genres Relations'])
# The routes related to movie ratings given by users
app.include_router(ratings.router,tags=['Ratings'])
# The routes related to movie recommendations given to users
app.include_router(recommendations.router,tags=['Recommendations'])
# The routes related to login of users, admins and ais
app.include_router(auth.router,tags=['Login'])

#DEBUG

# The admin-related routes
# app.include_router(admins.router,tags=['Admins'])

# The ai-related routes
# app.include_router(ais.router,tags=['Ais'])
