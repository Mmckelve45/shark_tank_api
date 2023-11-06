from enum import Enum
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
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


class Category(str, Enum):
    food = "Food & Beverage"
    tech = "Software/Tech"
    children = "Children"
    services = "Services"
    clothing = "Clothing/Fashion"
    lifestyle = "Lifestyle/Home"
    education = "Education"
    accessories = "Accessories/Gadgets"
    fitness = "Fitness/Outdoors"
    pet = "Pet products"
    cosmetics = "Cosmetics/Beauty"
    health = "Health/Self Care"
    travel = "Travel/Auto"
    media = "Media/Entertainment"
    other = "Other"


class Gender(str, Enum):
    male = 'Male'
    female = 'Female'
    hybrid = 'Hybrid'


class Shark(str, Enum):
    mc = "Mark Cuban"
    lg = "Lori Greiner"
    dj = "Daymond John"
    kl = "Kevin O’Leary"
    rh = "Robert Herjavec"
    bc = "Barbara Corcoran"
    eg = "Emma Grede"
    kh = "Kevin Hart"
    pj = "Peter Jones"
    dl = "Daniel Lubetzky"
    nt = "Nirav Tolia"
    kha = "Kevin Harrington"
    cs = "Chris Sacca"
    jf = "Jeff Foxworthy"
    jpd = "John Paul Dejoria"
    st = "Steve Tisch"
    nw = "Nick Woodman"
    ak = "Ashton Kutcher"
    tc = "Troy Carter"
    rb = "Richard Branson"
    ro = "Rohan Oza"
    ar = "Alex Rodriguez"
    sb = "Sara Blakely"
    bf = "Bethenny Frankel"
    js = "Jamie Siminoff"
    mh = "Matt Higgins"
    cb = "Charles Barkley"
    aw = "Alli Webb"
    awo = "Anne Wojcicki"
    ms = "Maria Sharapova"
    kla = "Katrina Lake"
    bm = "Blake Mycoskie"
    ks = "Kendra Scott"
    gp = "Gwyneth Paltrow"
    tx = "Tony Xu"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_pitches(db: db_dependency):
    try:
        return db.query(Pitches).order_by(Pitches.pitch_id.asc()).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        # You may want to customize the error message based on the exception


@router.get("/name", status_code=status.HTTP_200_OK)
async def get_pitches_by_name(db: db_dependency, name: str):
    try:
        return db.query(Pitches).filter(Pitches.name.ilike(f"%{name}%")).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/category", status_code=status.HTTP_200_OK)
async def get_pitches_by_category(db: db_dependency, category: Category):
    try:
        return db.query(Pitches).filter(Pitches.category == category).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/gender", status_code=status.HTTP_200_OK)
async def get_pitches_by_entrepreneur_gender(db: db_dependency, gender: Gender):
    try:
        return db.query(Pitches).filter(Pitches.entrepreneur_gender == gender).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/deal", status_code=status.HTTP_200_OK)
async def get_pitches_by_deal_made_or_not(db: db_dependency, is_deal: bool):
    try:
        return db.query(Pitches).filter(Pitches.is_deal == is_deal).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/shark", status_code=status.HTTP_200_OK)
async def get_pitches_by_shark_investor(db: db_dependency, investor: Shark):
    try:
        return db.query(Pitches).filter(Pitches.investors.any(investor)).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/{pitch_id}", status_code=status.HTTP_200_OK)
async def get_pitch_by_id(db: db_dependency, pitch_id: int = Path(gt=0)):
    try:
        return db.query(Pitches).filter(Pitches.pitch_id == pitch_id).first()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.get("/season/{season_id}", status_code=status.HTTP_200_OK)
async def get_pitches_by_season(db: db_dependency, season_id: int = Path(gt=0)):
    try:
        return db.query(Pitches).filter(Pitches.season_id == season_id).all()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")


@router.post('/', include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def create_pitch(
                      db: db_dependency,
                      pitch_request: Pitch):
    print(pitch_request)

    pitch_model = Pitches(**pitch_request.model_dump())
    db.add(pitch_model)
    db.commit()


@router.post('/load_data', include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def bulk_load_pitches(
                      db: db_dependency):
    pitch_data = 'assets/pitch_data.json'
    with open(pitch_data, 'r') as file:
        data = json.load(file)

    for pitch in data:
        new_pitch = Pitches(
            pitch_id=pitch['pitch_id'],
            name=pitch['name'],
            season_id=pitch['season_id'],
            episode=pitch['episode'],
            air_date=pitch['air_date'],
            summary=pitch['summary'],
            entrepreneur_gender=pitch['entrepreneur_gender'],
            entrepreneur=pitch['entrepreneur'],
            is_deal=pitch['is_deal'],
            ask_amt=pitch['ask_amt'],
            ask_perc=pitch['ask_perc'],
            ask_valuation=pitch['ask_valuation'],
            ask_summary=pitch['ask_summary'],
            deal_amt_equity=pitch['deal_amt_equity'],
            deal_perc_equity=pitch['deal_perc_equity'],
            deal_amt_debt=pitch['deal_amt_debt'],
            deal_valuation=pitch['deal_valuation'],
            deal_summary=pitch['deal_summary'],
            bite=pitch['bite'],
            investors=pitch['investors'],
            deal_structure=pitch['deal_structure'],
            category=pitch['category'],
            status=pitch['status'],
            website=pitch['website']
        )

        db.add(new_pitch)
    db.commit()

