from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder 
from fastapi import APIRouter


routerMovie = APIRouter()


class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
  overview: str = Field(default='Descripción de la pelicula', min_length=15, max_length=60)
  year: int = Field(default=2025)
  raiting: float = Field(ge=1, le=10)
  category: str = Field(default='Categoría de la película', min_length=3, max_length=15)

class BearerJWT(HTTPBearer):
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validateToken(auth.credentials)
    if data['email'] != 'pedro@gmail.com':
      raise HTTPException(status_code = 403, detail = 'Credenciales invalidas') 



@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
  db = Session()
  data = db.query(ModelMovie).all()
  # return JSONResponse(content=movies)
  return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message': 'Recruso no encontrado'})
  return JSONResponse(status_code=200, content=jsonable_encoder(data) )
  # for item in movies:
  #   if item ['id'] == id:
  #     return item
  #return []

@routerMovie.get('/movies/', tags=['Movies'], status_code=200)
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.category == category).first()
  if not data:
    return JSONResponse(status_code = 404, content={'message': 'No se encontro del recurso'})  
  return JSONResponse(status_code=200, content=jsonable_encoder(data))
  #return category

@routerMovie.post('/movies/', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newmovie = ModelMovie(**movie.dict())
    db.add(newmovie)
    db.commit()
    # movies.append(movie)
    # print(movies)
    # return JSONResponse(content={'message':'Se ha insetado una nueva película', 'movie':dict(movie)}) Forma mía
    # return JSONResponse(status_code=201, content={'message':'Se ha insetado una nueva película', 'movie':[movie.dict() for m in movies]}) #forma del prof
    return JSONResponse(status_code=201, content={'message':'Se ha insetado una nueva película'})

@routerMovie.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie: Movie):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code = 404, content={'message': 'No se encontro del recurso'})
  data.title = movie.title
  data.overview = movie.overview
  data.year = movie.year
  data.raiting = movie.raiting
  data.category = movie.category
  db.commit()
  return JSONResponse(content={'message': 'Se ha modificado la película'})
  
  # for item in movies:
  #   if item["id"] == id:
  #     item ['title'] = movie.title,
  #     item ['overview'] = movie.overview,
  #     item ['year'] = movie.year,
  #     item ['raiting'] = movie.raiting,
  #     item ['category'] = movie.category,
  #     return JSONResponse(content={'message': 'Se ha modificado la película'})

@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id:int):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code = 404, content={'message': 'No se encontro del recurso'})
  db.delete(data)
  db.commit()
  return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula', 'data': jsonable_encoder(data)})
  # print(movies)
  # for item in movies:
  #   if item ["id"] == id:
  #     movies.remove(item)
  #     print(movies)
  #     return JSONResponse(content={'message': 'Se ha eliminado la película'})