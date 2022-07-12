from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import PostBase, PostDisplay, UpdatePost
from db.database import get_db
from db import db_post
from typing import List
import random
import string
import shutil
import json
from routers.schemas import UserAuth
from db import models


router = APIRouter(
  prefix='/post',
  tags=['post']
)

image_url_types = ['absolute', 'relative']

@router.post('/create_movie', response_model=PostDisplay)
# def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
def create(request: PostBase, db: Session = Depends(get_db)):
  if not request.image_url_type in image_url_types:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
  return db_post.create(db, request)

@router.get('/all', status_code=status.HTTP_200_OK)
def posts(db: Session = Depends(get_db)):
  movies = db.query(models.DbPost).all()
  return movies

@router.get('/movie/{id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(id:int, db:Session = Depends(get_db)):
    movie = db.query(models.DbPost).filter(models.DbPost.id == id).first()
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id : {id} not found")
    return movie


@router.get('/get_movie/{id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(id: int, db: Session = Depends(get_db)):
      movie = db.query(models.DbPost).filter(models.DbPost.id == id).first()
      if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {id} does not exist")
      return movie

@router.get('/get_movie_user_id/{user_id}', status_code=status.HTTP_200_OK)
def get_movie_user_id(user_id: int, db: Session = Depends(get_db)):
      movie = db.query(models.DbPost).filter(models.DbPost.user_id == user_id).all()
      if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with user id {id} does not exist")
      return movie

@router.post("/submit")
async def submit(base: PostBase = Depends(), files: List[UploadFile] = File(...)):
    received_data= base.dict()
    return {"JSON Payload ": received_data, "Filenames": [file.filename for file in files]}
 

@router.post("/uploadfiles/")
def create_upload_files(upload_file: UploadFile = File(...)):
    json_data = json.load(upload_file.file)
    return {"data_in_file": json_data}


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  
  return {'filename': path}


@router.get('/movie/{caption}')
def get_movie_by_caption(caption: str, db: Session = Depends(get_db)):
      movie_caption = db.query(models.DbPost).filter(models.DbPost.caption == caption).all()
      if movie_caption is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie Does Not Exist with Movie Caption {caption}")
      return movie_caption


@router.get('/movie/{name}')
def get_movie_by_name(name: str, db: Session = Depends(get_db)):
      movie_name = db.query(models.DbPost).filter(models.DbPost.name == name).all()
      if movie_name is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie Does Not Exist with Movie Caption {caption}")
      return movie_name


@router.get('/movie/{popularity}')
def get_movie_by_popularity(popularity: float, db: Session = Depends(get_db)):
      movie_popularity = db.query(models.DbPost).filter(models.DbPost.popularity == popularity).all()
      if movie_popularity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie Does Not Exist with Movie Name {popularity}")
      return movie_popularity


@router.get('/movie/{director}')
def get_movie_by_director(director: str, db: Session = Depends(get_db)):
      movie_director = db.query(models.DbPost).filter(models.DbPost.director == director).all()
      if movie_director is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie Does Not Exist with Director {director}")
      return movie_director


@router.get('/movie/{imdb_score}')
def get_movie_by_imdb_score(imdb_score: float, db: Session = Depends(get_db)):
      movie_score = db.query(models.DbPost).filter(models.DbPost.imdb_score == imdb_score).all()
      if movie_score is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie Does Not Exist with Director {imdb_score}")
      return movie_score


@router.put('/update/{id}', status_code=status.HTTP_200_OK, response_model=PostDisplay)
def update_movie(id: int, Post: PostDisplay, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
      update_post = db.query(models.DbPost).filter(models.id==id)
      update = update_post.first()
      if update == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
      update_post.update(Post.dict(), synchronize_session=False)


@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_post.delete(db, id, current_user.id)
