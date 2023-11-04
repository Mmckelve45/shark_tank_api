from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Pitches
import json


router = APIRouter(
    prefix='/pitches',
    tags=['pitches']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Pitch(BaseModel):
    pitch_id: int
    name: str
    season_id: int
    episode_id: int
    air_date: str
    summary: str
    entrepreneur_gender: str
    entrepreneur: List[str]
    is_deal: bool
    ask_amt: int
    ask_perc: float
    ask_valuation: int
    ask_summary: str
    deal_amt_equity: int
    deal_perc_equity: float
    deal_amt_debt: int
    deal_valuation: int
    deal_summary: str
    bite: int
    investors: List[str]
    deal_structure: List[str]
    category: str
    status: str
    website: str


class OldPitch(BaseModel):
    id: int
    name: str
    season: int
    episode: int
    airDate: str
    businessPitch: str
    entrepreneurGender: str
    entrepreneur: List[str]
    isDeal: bool
    askAmt: int
    askPerc: float
    askValuation: int
    askSummary: str
    dealAmtEquity: int
    dealPercEquity: float
    dealAmtDebt: int
    dealValuation: int
    dealSummary: str
    bite: int
    shark: List[str]
    dealStructure: List[str]
    category: str
    status: str
    website: str
    hasAmazonLink: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_pitches(db: db_dependency):
    return db.query(Pitches).order_by(Pitches.pitch_id.asc()).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency,
                      pitch_request: Pitch):
    print(pitch_request)

    pitch_model = Pitches(**pitch_request.model_dump())
    db.add(pitch_model)
    db.commit()


@router.post('/load_data', status_code=status.HTTP_201_CREATED)
async def create_episode(
                      db: db_dependency):

    pitch_data = 'assets/pitch_data.json'
    with open(pitch_data, 'r') as file:
        data = json.load(file)
    for pitch in data:

        # if pitch['id'] == 4:
        #     break

        sharks = []
        for i in pitch['shark']:
            if i != "":
                sharks.append(i)

        structure = []
        for v in pitch['dealStructure']:
            if v != "":
                structure.append(v)
        ent = []
        for t in pitch['entrepreneur']:
            if t != "":
                ent.append(t)


        # x = pitch['test'] if pitch['test'] != "" else None
        print(pitch['id'])

        new_pitch = Pitches(
            pitch_id=int(pitch['id']) + 1,
            name=pitch['name'],
            season_id=int(pitch['season']),
            episode_id=int(pitch['episode']),
            air_date=pitch['airDate'],
            summary=pitch['businessPitch'],
            entrepreneur_gender=pitch['entrepreneurGender'],
            entrepreneur=ent,
            is_deal=pitch['isDeal'],
            ask_amt=int(pitch['askAmt'].replace(",", "")),
            ask_perc=float(pitch['askPerc']) if pitch['askPerc'] is not None else None,
            ask_valuation=int(pitch['askValuation'].replace(",", "")),
            ask_summary=pitch['askSummary'],
            deal_amt_equity=int(pitch['dealAmtEquity'].replace(",", "")) if pitch['dealAmtEquity'] != "" else None,
            deal_perc_equity=float(pitch['dealPercEquity']) if pitch['dealPercEquity'] is not None else None,
            deal_amt_debt=int(pitch['dealAmtDebt'].replace(",", "")) if pitch['dealAmtDebt'] != "" else None,
            deal_valuation=int(pitch['dealValuation'].replace(",", "")) if pitch['dealValuation'] != "" else None,
            deal_summary=pitch['dealSummary'] if pitch['dealSummary'] != "" else None,
            bite=int(pitch['bite'].replace(",", "")) if pitch['dealSummary'] != "" else None,
            investors=sharks,
            deal_structure=structure,
            category=pitch['category'],
            status=pitch['status'],
            website=pitch['website']
        )

        db.add(new_pitch)
    db.commit()

