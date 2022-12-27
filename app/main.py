from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapibackend",
            user="root",
            password="password",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
