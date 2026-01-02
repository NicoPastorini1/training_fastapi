from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    category: str
    year: int
    stars: float
