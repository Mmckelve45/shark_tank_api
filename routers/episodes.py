from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Episodes, Shark
import json


router = APIRouter(
    prefix='/episodes',
    tags=['episodes']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Company(BaseModel):
    name: str
    isDeal: bool
    id: int

    # to_dict just made my life easier on initial load with unformatted data
    def to_dict(self):
        return {
            "name": self.name,
            "isDeal": self.isDeal,
            "id": self.id
        }


class Episode(BaseModel):
    episode_id: int
    sharks: List[str]
    season_id: int
    episode: int
    episode_all: int
    title: str
    date: str
    wikipedia_url: str
    companies: List[Company]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_episodes(db: db_dependency):
    try:
        return db.query(Episodes).order_by(Episodes.episode_id.asc()).all()
    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # print(f"Error: {str(e)}")
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")
        # You may want to customize the error message based on the exception


@router.get("/shark", status_code=status.HTTP_200_OK)
async def get_episodes_by_shark_involved(db: db_dependency, shark: Shark):
    try:
        return db.query(Episodes).filter(Episodes.sharks.any(shark)).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")


@router.get("/season/{season_id}", status_code=status.HTTP_200_OK)
async def get_episodes_by_season(db: db_dependency, season_id: int = Path(gt=0)):
    try:
        return db.query(Episodes).filter(Episodes.season_id == season_id).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")


@router.get("/{episode_id}", status_code=status.HTTP_200_OK)
async def get_episode_by_id(db: db_dependency, episode_id: int = Path(gt=0)):
    try:
        return db.query(Episodes).filter(Episodes.episode_id == episode_id).first()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")


@router.post('/', include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency,
                      episode_request: Episode):
    episode_model = Episodes(**episode_request.model_dump())
    db.add(episode_model)
    db.commit()


@router.post('/load_data', include_in_schema=True, status_code=status.HTTP_201_CREATED)
async def bulk_load_episodes(
                      db: db_dependency):
    episode_data = 'assets/episode_data.json'
    with open(episode_data, 'r') as file:
        data = json.load(file)

    # Need to re-upload and increment the id in companies by 1
    for ep in data:

        # Increment company IDs by 1
        for company in ep['companies']:
            company['id'] += 1

        new_ep = Episodes(
            episode_id=ep['episode_id'],
            sharks=ep['sharks'],
            season_id=ep['season_id'],
            episode=ep['episode'],
            episode_all=ep['episode_all'],
            title=ep['title'],
            date=ep['date'],
            wikipedia_url=ep['wikipedia_url'],
            # companies=ep['companies']
        )

        # Create Companies instances using to_dict method
        companies = [
            Company(**company).to_dict()
            for company in ep['companies']
        ]
        new_ep.companies = companies
        db.add(new_ep)
    db.commit()
