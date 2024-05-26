from typing import Dict, Any

import requests
from src.config import TMDB_API, BASE_URL
import httpx
from fastapi import HTTPException


class APIFunctions:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}search/movie?api_key={self.api_key}&language=en-US&page=1&include_adult=false&query={query}"
            )
            return response.json()

    async def get_popular_movies(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}trending/movie/week?api_key={self.api_key}")
            data = response.json()
            return data["results"]

    async def get_movie_details(self, movie_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}movie/{movie_id}?api_key={self.api_key}&language=en-US")
            data = response.json()

            return data

    async def get_movie_brief_data(self, movie_id: int) -> dict[str, Any] | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}movie/{movie_id}?api_key={self.api_key}&language=en-US"
            )
            data = response.json()

            return {
                "title": data.get("title"),
                "overview": data.get("overview"),
                "vote_average": data.get("vote_average"),
                "backdrop_path": data.get("backdrop_path")
            }


TMDB = APIFunctions(TMDB_API)
