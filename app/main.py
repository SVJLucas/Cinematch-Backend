from database.database import connect_to_database
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()
db = connect_to_database()
print(db.get())





