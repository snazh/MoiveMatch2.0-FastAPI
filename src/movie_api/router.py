from fastapi import APIRouter, status, HTTPException
from src.movie_api.service import TMDB
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/movie_api",
    tags=["Movie API"]
)


@router.get("/trends", status_code=status.HTTP_200_OK)
@cache(expire=3600)
async def get_popular_movies():
    try:
        trends = await TMDB.get_popular_movies()
        return {
            "status": "success",
            "data": trends,
            "details": "The movies were found successfully"
        }
    except ValueError:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Trends searching aborted"
        })


@router.get("/movie/{movie_id}", status_code=status.HTTP_200_OK)
async def get_specific_movie(movie_id: int):
    try:
        movie_details = await TMDB.get_movie_details(movie_id)
        if movie_details["status"] == "error":
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Movie does not exist"
            })
        return {
            "status": "success",
            "data": movie_details,
            "details": "The movies were found successfully"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Movie with i:{movie_id} does not exist"
        })


@router.get("/search/{query}", status_code=status.HTTP_200_OK)
async def search_movies(query: str):
    try:

        search_result = await TMDB.search(query)
        return {
            "status": "success",
            "data": search_result,
            "details": "The movies were found successfully"
        }
    except ValueError:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Error occurred while searching movies"
        })


@router.get("/brief-data/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie_brief_data(movie_id: int):
    try:
        movie_details = await TMDB.get_movie_brief_data(movie_id)
        if movie_details["title"] is None:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Movie does not exist"
            })
        return {
            "status": "success",
            "data": movie_details,
            "details": "The movies were found successfully"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Movie with id:{movie_id} does not exist"
        })
