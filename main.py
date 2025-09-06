import os
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Header
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


def verify_admin_api_key(x_admin_api_key: str = Header(...)):
    """
    Verify the admin API key for protected operations.
    Set ADMIN_API_KEY environment variable to secure this endpoint.
    """
    expected_api_key = os.getenv("ADMIN_API_KEY")
    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin operations are not configured. Set ADMIN_API_KEY environment variable."
        )
    
    if x_admin_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin API key"
        )


# Bulk load all the data into the database.  Sharks, Seasons, Episodes, and Pitches
# This endpoint is protected with admin API key authentication.
# Set ADMIN_API_KEY environment variable and include 'X-Admin-API-Key' header in requests.
@app.post('/bulk_load_data', include_in_schema=True, status_code=status.HTTP_201_CREATED)
async def bulk_load_data(
    db: db_dependency,
    admin_key: str = Depends(verify_admin_api_key)
):
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
