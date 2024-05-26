from pathlib import Path
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
import uvicorn
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.auth.base_config import auth_backend, get_current_user_or_redirect
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.movie_api.router import router as movie_api
from src.friend_system.router import router as friend_system_router
from src.movie_algo.router import router as movie_algo_router
from src.pages.router import router as router_pages
from fastapi.responses import RedirectResponse, JSONResponse
from src.user_managment.router import router as user_router
from src.config import REDIS_HOST

app = FastAPI(
    title="Movie Match"
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(user_router)
app.include_router(movie_api)
app.include_router(friend_system_router)
app.include_router(movie_algo_router)

app.mount("/src", StaticFiles(directory=Path(__file__).parent.parent / "src"), name="static")
app.include_router(router_pages)
current_user = fastapi_users.current_user()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/pages/login")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/protected-route")
async def protected_route(user=Depends(get_current_user_or_redirect)):
    if isinstance(user, RedirectResponse):
        return user
    return {"message": f"Hello, {user.email}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
