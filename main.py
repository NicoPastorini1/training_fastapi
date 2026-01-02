from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from excel_service import (
    ensure_excel_exists,
    read_all_movies,
    read_movie_by_id,
    insert_movie,
    delete_movie_by_id
)
from schemas.movie import Movie


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_excel_exists()
    yield


app = FastAPI(lifespan=lifespan)


# GET /movies
@app.get("/movies", response_model=list[Movie], tags=["Movies"])
def get_movies():
    return read_all_movies()


# GET /movies/{id}
@app.get("/movies/{movie_id}", response_model=Movie, tags=["Movies"])
def get_movie(movie_id: int):
    movie = read_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# POST /movies
@app.post("/movies", status_code=201, tags=["Movies"])
def create_movie(movie: Movie):
    try:
        insert_movie(
            id=movie.id,
            title=movie.title,
            category=movie.category,
            year=movie.year,
            stars=movie.stars
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return movie

@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    movie = delete_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie