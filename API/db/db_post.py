from fastapi import HTTPException, status
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm.session import Session
from db.models import DbPost
import datetime


def create(db: Session, request: PostBase):
  new_post = DbPost(
    image_url = request.image_url,
    image_url_type = request.image_url_type,
    popularity = request.popularity,
    director = request.director,
    caption = request.caption,
    imdb_score = request.imdb_score,
    name = request.name,
    timestamp = datetime.datetime.now(),
    user_id = request.creator_id
  )

  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

def get_all(db: Session, request: PostBase):
      return db.query(DbPost).all()


def delete(db: Session, id: int, user_id: int):
  post = db.query(DbPost).filter(DbPost.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'Post with id {id} not found')
  if post.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only post creator can delete post')

  db.delete(post)
  db.commit()
  return 'ok'