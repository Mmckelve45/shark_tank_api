from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Sharks
import json


router = APIRouter(
    prefix='/sharks',
    tags=['sharks']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Shark(BaseModel):
    shark_id: int
    name: str
    summary: str
    description: str
    img: str
    is_guest: str
    dob: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_sharks(db: db_dependency):
    return db.query(Sharks).order_by(Sharks.shark_id.asc()).all()


@router.post('/load_data', status_code=status.HTTP_201_CREATED)
async def bulk_load_sharks(
                      db: db_dependency):

    shark_data = 'assets/investor_data_old.json'
    with open(shark_data, 'r') as file:
        data = json.load(file)
    ind = 1
    for shark in data:

        temp_guest = True
        if shark['name'] == 'Mark Cuban' or \
                shark['name'] == 'Barbara Corcoran' or \
                shark['name'] == 'Daymond John' or \
                shark['name'] == "Kevin O'Leary" or \
                shark['name'] == 'Robert Herjavec' or \
                shark['name'] == 'Lori Greiner':
            temp_guest = False

        new_shark = Sharks(
            shark_id=ind,
            name=shark['name'],
            summary=shark['summary'],
            description=shark['description'],
            img=shark['img'],
            is_guest=temp_guest,
            dob=shark['dob']
        )
        db.add(new_shark)
        ind += 1
    db.commit()


@router.post('/load_data_new', status_code=status.HTTP_201_CREATED)
async def bulk_load_sharks(
                      db: db_dependency):

    shark_data = 'assets/investor_data.json'
    with open(shark_data, 'r') as file:
        data = json.load(file)
    # ind = 1
    for shark in data:

        # temp_guest = True
        # if shark['name'] == 'Mark Cuban' or \
        #         shark['name'] == 'Barbara Corcoran' or \
        #         shark['name'] == 'Daymond John' or \
        #         shark['name'] == "Kevin O'Leary" or \
        #         shark['name'] == 'Robert Herjavec' or \
        #         shark['name'] == 'Lori Greiner':
        #     temp_guest = False

        new_shark = Sharks(
            shark_id=shark['shark_id'],
            name=shark['name'],
            summary=shark['summary'],
            description=shark['description'],
            img=shark['img'],
            is_guest=shark['is_guest'],
            dob=shark['dob']
        )
        db.add(new_shark)
    db.commit()