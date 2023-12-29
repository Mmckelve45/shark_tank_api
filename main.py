from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from starlette import status

import models
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from routers import episodes, pitches, sharks, seasons
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# If you want to run this locally and have another local application call it you need to specify cors
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# only is run if the database does not exist
models.Base.metadata.create_all(bind=engine)

app.include_router(sharks.router)
app.include_router(seasons.router)
app.include_router(episodes.router)
app.include_router(pitches.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Bulk load all the data into the database.  Sharks, Seasons, Episodes, and Pitches
# You should call when you run the application for the first time once you have configured your databaseURL
# This populates your PostgresDB with all the data in the assets folder.
@app.post('/bulk_load_data', include_in_schema=True, status_code=status.HTTP_201_CREATED)
async def bulk_load_data(db: db_dependency):
    try:

        await seasons.bulk_load_seasons(db)
        await sharks.bulk_load_sharks(db)
        # need to load seasons before episodes because season_id is a Foreign Key
        await episodes.bulk_load_episodes(db)
        # need to load seasons before pitches because season_id is a Foreign Key
        await pitches.bulk_load_pitches(db)

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error on bulk load: {str(e)}")
        # You may want to customize the error message based on the exception

    return
