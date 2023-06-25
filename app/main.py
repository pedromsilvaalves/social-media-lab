import time
import psycopg2

from psycopg2.extras import RealDictCursor
from fastapi import FastAPI

from . import models
from .database import engine

from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DIRECT DATABASE CONNECTION METHOD DEPENDENCY
is_database_connected = False

while not is_database_connected:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="socialmediadb",
            user="postgres",
            password="Senhapsql123",
            port=5432,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        is_database_connected = True
        print("Database connection was succesfull")
    except Exception as error:
        print("Database connection failed. Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)