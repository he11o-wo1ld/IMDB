from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends, status
from db import models
from db.database import get_db
from db import db_user

router = APIRouter(
  prefix='/user',
  tags=['user']
)

@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
  return db_user.create_user(db, request)


@router.get('/all', status_code=status.HTTP_200_OK)
def posts(db: Session = Depends(get_db)):
  user = db.query(models.DbUser).all()
  return user
