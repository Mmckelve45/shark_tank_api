from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
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
    try:
        return db.query(Sharks).order_by(Sharks.shark_id.asc()).all()
    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")
        # You may want to customize the error message based on the exception


@router.get("/age", status_code=status.HTTP_200_OK)
async def sort_all_sharks_by_age_oldest_to_youngest(db: db_dependency):
    try:
        return db.query(Sharks).order_by(Sharks.dob.asc()).all()
    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")
        # You may want to customize the error message based on the exception


@router.get("/{shark_id}", status_code=status.HTTP_200_OK)
async def get_shark_by_id(db: db_dependency, shark_id: int = Path(gt=0)):
    try:
        return db.query(Sharks).filter(Sharks.shark_id == shark_id).first()

    except Exception as e:
        # Handle exceptions and set an appropriate status code
        # raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again! {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something went wrong.  Please try again!")


@router.post('/load_data', include_in_schema=True, status_code=status.HTTP_201_CREATED)
async def bulk_load_sharks(
                      db: db_dependency):

    shark_data = 'assets/shark_data.json'
    with open(shark_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for shark in data:
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
