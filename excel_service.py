from pathlib import Path
import pandas as pd

excel_name = Path("IMDb Movies.xlsx")
COLUMNS = ["id", "title", "category", "year", "stars"]


def ensure_excel_exists() -> None:
    if not excel_name.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(excel_name, index=False)


def _read_df() -> pd.DataFrame:
    ensure_excel_exists()
    return pd.read_excel(excel_name)


def read_all_movies() -> list[dict]:
    df = _read_df()
    return df.to_dict(orient="records")


def read_movie_by_id(movie_id: int) -> dict | None:
    df = _read_df()
    result = df[df["id"] == movie_id]
    if result.empty:
        return None
    return result.iloc[0].to_dict()

def insert_movie(
    id: int,
    title: str,
    category: str,
    year: int,
    stars: int
) -> None:
    df = _read_df()

    if (df["id"] == id).any():
        raise ValueError(f"Ya existe una película con id={id}")

    new_row = pd.DataFrame([{
        "id": id,
        "title": title,
        "category": category,
        "year": year,
        "stars": stars
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(excel_name, index=False)

def delete_movie_by_id(movie_id: int) -> dict | None:
    df = _read_df()

    result = df[df["id"] == movie_id]
    if result.empty:
        return None

    deleted_movie = result.iloc[0].to_dict()
    df = df[df["id"] != movie_id]
    df.to_excel(excel_name, index=False)

    return deleted_movie

def update_movie_by_id(
    id: int,
    title: str,
    category: str,
    year: int,
    stars: int) -> dict | None:
    
    df = _read_df()
    
    mask = df["id"] == id
    
    if not mask.any():
        return None
    
    old_movie = df.loc[mask].iloc[0].to_dict()
    
    df.loc[mask, title] = title
    df.loc[mask, category] = category
    df.loc[mask, year] = year
    df.loc[mask, stars] = stars
    
    _write_df = (df)
    
    return old_movie