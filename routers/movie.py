from fastapi import APIRouter, Path, Query, Depends
from models.movie import Movie as MovieModel
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model = List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model= Movie, status_code=200)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = {'message': "No encontrado"})
    return JSONResponse(status_code=200, content = jsonable_encoder(result))
    

# Si no se especifica el parametor en la ruta , FastAPI lo toma como parametro de Query
@movie_router.get('/movies/category/', tags=['movies'], response_model= List[Movie], status_code = 200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=50)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.get('/movies/year/', tags=['movies'], response_model= List[Movie], status_code = 200)
def get_movies_by_year(year: str = Query(min_length=4, max_length=5)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_year(year)
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code = 201, content = {"message" : "Se registró la película correctamente"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = {'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code = 200, content = {"message" : "Se edito la película correctamente"})
        
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {'message': "No encontrado"})
    
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code = 200, content = {"message" : "Se eliminó la película correctamente"})