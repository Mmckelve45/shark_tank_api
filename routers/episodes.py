from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Episodes
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
    # def to_dict(self):
    #     return {
    #         "name": self.name,
    #         "isDeal": self.isDeal,
    #         "id": self.id
    #     }


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
    return db.query(Episodes).order_by(Episodes.episode_id.asc()).all()


@router.post('/', include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency,
                      episode_request: Episode):
    episode_model = Episodes(**episode_request.model_dump())
    db.add(episode_model)
    db.commit()


@router.post('/load_data', include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def bulk_load_episodes(
                      db: db_dependency):
    episode_data = 'assets/episode_data.json'
    with open(episode_data, 'r') as file:
        data = json.load(file)

    for ep in data:
        new_ep = Episodes(
            episode_id=ep['episode_id'],
            sharks=ep['sharks'],
            season_id=ep['season_id'],
            episode=ep['episode'],
            episode_all=ep['episode_all'],
            title=ep['title'],
            date=ep['date'],
            wikipedia_url=ep['wikipedia_url'],
            companies=ep['companies']
        )
        db.add(new_ep)
    db.commit()
