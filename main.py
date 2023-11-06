from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from starlette import status

import models
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from routers import episodes, pitches, sharks, seasons
app = FastAPI()

# only is run if the todos.db does not exist
models.Base.metadata.create_all(bind=engine)

app.include_router(episodes.router)
app.include_router(pitches.router)
app.include_router(sharks.router)
app.include_router(seasons.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/bulk_load_data', include_in_schema=False, status_code=status.HTTP_201_CREATED)
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

