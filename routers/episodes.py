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


class OldEpisode(BaseModel):
    sharks: List[str]
    pitches: List[str]
    season: int
    episode: int
    episodeAll: int
    title: str
    date: str
    viewers: str
    url: str
    companies: List[Company]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_episodes(db: db_dependency):
    return db.query(Episodes).order_by(Episodes.episode_id.asc()).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency,
                      episode_request: Episode):
    print(episode_request)
    # companies_json = json.dumps(episode_request.companies)
    # episode_data = episode_request.model_dump()
    # episode_data['companies'] = companies_json

    episode_model = Episodes(**episode_request.model_dump())
    # episode_model['companies'] = companies_json
    db.add(episode_model)
    db.commit()


@router.post('/bulk', status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency,
                      episode_request: List[OldEpisode]):

    for ep in episode_request:

        companies = []
        for i in ep.companies:
            companies.append(i.to_dict())



        new_ep = Episodes(
            episode_id=int(ep.episodeAll),
            sharks=ep.sharks,
            season_id=int(ep.season),
            episode=int(ep.episode),
            episode_all=int(ep.episodeAll),
            title=ep.title,
            date=ep.date,
            wikipedia_url=ep.url,
            companies=companies
        )
        db.add(new_ep)
    db.commit()

# DO NOT DELETE
# @router.post('/load_data', status_code=status.HTTP_201_CREATED)
# async def create_episode(
#                       db: db_dependency):
#
#     episode_data = 'assets/episode_data.json'
#     with open(episode_data, 'r') as file:
#         data = json.load(file)
#     for ep in data['episodes']:
#
#         companies = []
#         for i in ep['companies']:
#             companies.append(i)
#
#         new_ep = Episodes(
#             episode_id=int(ep['episodeAll']),
#             sharks=ep['sharks'],
#             season_id=int(ep['season']),
#             episode=int(ep['episode']),
#             episode_all=int(ep['episodeAll']),
#             title=ep['title'],
#             date=ep['date'],
#             wikipedia_url=ep['url'],
#             companies=companies
#         )
#         db.add(new_ep)
#     db.commit()



