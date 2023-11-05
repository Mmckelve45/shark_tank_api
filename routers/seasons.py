from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Seasons
import json


router = APIRouter(
    prefix='/seasons',
    tags=['seasons']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Season(BaseModel):
    season_id: int
    num_episodes: int
    summary: str
    shark_info: str
    start_date: str
    end_date: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_seasons(db: db_dependency):
    return db.query(Seasons).order_by(Seasons.season_id.asc()).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_season(
                      db: db_dependency,
                      season_request: Season):
    print(season_request)
    # companies_json = json.dumps(episode_request.companies)
    # episode_data = episode_request.model_dump()
    # episode_data['companies'] = companies_json

    season_model = Seasons(**season_request.model_dump())
    # episode_model['companies'] = companies_json
    db.add(season_model)
    db.commit()


@router.post('/load_data_new', status_code=status.HTTP_201_CREATED)
async def bulk_load_seasons(
                      db: db_dependency):
    print('made it here')

    season_data = 'assets/season_data.json'
    with open(season_data, 'r') as file:
        data = json.load(file)
    for seas in data:
        # print(seas['season_id'])
        # print(seas['num_episodes'])
        # print(seas['summary'])
        # print(seas['shark_info'])
        # print(seas['start_date'])
        # print(seas['end_date'])
        # season_model = Seasons(**seas.model_dump())

        new_seas = Seasons(
            season_id=seas['season_id'],
            num_episodes=seas['num_episodes'],
            summary=seas['summary'],
            shark_info=seas['shark_info'],
            start_date=seas['start_date'],
            end_date=seas['end_date'],
        )
        db.add(new_seas)
    db.commit()
