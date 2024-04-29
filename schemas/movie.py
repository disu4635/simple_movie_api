from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: str = Field(min_length=4, max_length=5)
    rating: float = Field(ge = 1, le=10)
    category: str = Field(default = "Una Película", min_length=5, max_length=50)

    class Config:
        json_schema_extra = {
            "example" : {
                "id": 1,
                "title": "Interestelar",
                "overview": "Pelicula sobre exploracion espacial",
                "year": "2014",
                "rating": 10.0,
                "category": "Ciencia ficcion, Drama"
            }
        }