from typing import List
from firebase_admin.db import Reference
from database.database import get_database
from fastapi import APIRouter, status, Depends

router = APIRouter()