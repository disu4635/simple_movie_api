from models.movie import Movie as MovieModel
from schemas.movie import Movie
from sqlalchemy.orm import Session

class MovieService():
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def get_movie_by_year(self, year):
        result = self.db.query(MovieModel).filter(MovieModel.year == year).all()
        return result
    
    def create_movie(self, movie: Movie):
        # Los ** al inicio extrae los atributos y los pasa como parametros
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return 
    
    def update_movie(self, id: int, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return
