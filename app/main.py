from fastapi import FastAPI
from routers import genres,movies,movies_genres
from database.database import connect_to_database
from dotenv import load_dotenv


# Carregar as variáveis do arquivo .env
load_dotenv()
app = FastAPI()
connect_to_database()


app.include_router(genres.router)
app.include_router(movies.router)
app.include_router(movies_genres.router)





