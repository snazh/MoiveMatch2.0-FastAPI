from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_users import exceptions

from src.movie_api.router import search_movies, get_specific_movie, get_popular_movies
from src.movie_algo.router import is_favorite, get_recommendations
from src.auth.router import get_profile
from src.auth.router import get_another_profile
router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/pages/templates")


@router.get("/trends", response_class=HTMLResponse)
async def get_trends(request: Request, popular_movies: dict = Depends(get_popular_movies)):
    trends = popular_movies['data']
    return templates.TemplateResponse("trends.html",
                                      {"request": request,
                                       "title": "Trends",
                                       "trends": trends
                                       })


@router.get("/catalog/{query}", response_class=HTMLResponse)
async def get_catalog_page(request: Request, movies: dict = Depends(search_movies)):
    print(True)
    search_results = movies["data"]["results"]
    return templates.TemplateResponse("catalog.html",
                                      {"request": request,
                                       "title": "Catalog",
                                       "search_results": search_results
                                       })


@router.get("/soulmate", response_class=HTMLResponse)
async def get_soulmate(request: Request, soulmate=Depends(get_recommendations)):
    recommendations = soulmate["data"]

    return templates.TemplateResponse("soulmate.html",
                                      {"request": request,
                                       "title": "Soulmate",
                                       "movies": recommendations['movies'],
                                       "soulmate": recommendations["soulmate"],
                                       "percentage": recommendations["percentage"]
                                       })


@router.get("/movie-overview/{movie_id}", response_class=HTMLResponse)
async def get_movie_overview(request: Request, movie_overview=Depends(get_specific_movie), button=Depends(is_favorite)):
    return templates.TemplateResponse("overview.html", {"request": request,
                                                        "movie_overview": movie_overview['data'],
                                                        "button_status": button["data"],
                                                        "title": movie_overview['data']['title']})


@router.get("/about-us", response_class=HTMLResponse)
async def get_about_us_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "page_title": "About"})


@router.get('/register', response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request,

                                                        "page_title": "Registration"})


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,

                                                     "page_title": "Login"})


@router.get('/profile', response_class=HTMLResponse)
async def own_profile(request: Request, user=Depends(get_profile)):
    data = user['data']
    return templates.TemplateResponse('user_profile.html', {"request": request,
                                                            "user": data,
                                                            "page_title": "Profile"})


@router.get("/another-profile/{user_id}", response_class=HTMLResponse)
async def profile(request: Request, user=Depends(get_another_profile)):
    data = user['data']
    return templates.TemplateResponse('user_profile.html', {"request": request,
                                                            "user": data,
                                                            "page_title": data['username']})
