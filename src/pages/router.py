from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.movie_api.router import search_movies, get_specific_movie, get_popular_movies
from src.movie_algo.router import is_favorite, get_recommendations
from src.user_managment.router import get_user_profile, get_my_profile, search_users

from src.friend_system.router import get_user_friends, friend_status

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
    search_results = movies["data"]["results"]
    return templates.TemplateResponse("catalog.html",
                                      {"request": request,
                                       "title": "Catalog",
                                       "search_results": search_results
                                       })


@router.get("/soulmate", response_class=HTMLResponse)
async def get_soulmate(request: Request,
                       soulmate: dict = Depends(get_recommendations)):
    recommendations = soulmate["data"]
    return templates.TemplateResponse("soulmate.html",
                                      {"request": request,
                                       "page_title": "Soulmate",
                                       "movies": recommendations['movies'],
                                       "soulmate": recommendations["soulmate"],
                                       "percentage": recommendations["percentage"]
                                       })


@router.get("/movie-overview/{movie_id}", response_class=HTMLResponse)
async def get_movie_overview(request: Request,
                             movie_overview: dict = Depends(get_specific_movie),
                             button: dict = Depends(is_favorite),
                             ):
    return templates.TemplateResponse("overview.html", {"request": request,
                                                        "movie_overview": movie_overview['data'],
                                                        "button_status": button["button_status"],
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


@router.get('/profile/{user_id}', response_class=HTMLResponse)
async def get_user_profile(request: Request,
                           user_profile: dict = Depends(get_user_profile),
                           friend: dict = Depends(friend_status)):
    movies = user_profile["data"]['movies']
    user_data = user_profile["data"]['user']
    is_friend = friend['is_friend']
    return templates.TemplateResponse('user_profile.html', {"request": request,
                                                            "movies": movies,
                                                            "user": {
                                                                "id": user_data[0],
                                                                "email": user_data[1],
                                                                "username": user_data[2],
                                                                "created_at": user_data[3]

                                                            },
                                                            "is_friend": is_friend,
                                                            "is_owner": False,
                                                            "page_title": "Profile"})


@router.get("/my-profile", response_class=HTMLResponse)
async def get_my_profile(request: Request,
                         user_profile=Depends(get_my_profile),
                         ):
    movies = user_profile["data"]['movies']
    user_data = user_profile["data"]['user']
    return templates.TemplateResponse('user_profile.html', {"request": request,
                                                            "movies": movies,
                                                            "user": {
                                                                "id": user_data[0],
                                                                "email": user_data[1],
                                                                "username": user_data[2],
                                                                "created_at": user_data[3]
                                                            },

                                                            "is_owner": True,
                                                            "page_title": "Profile"})


@router.get("/my-friends", response_class=HTMLResponse)
async def get_my_friends(request: Request,
                         friends: dict = Depends(get_user_friends),
                         ):
    return templates.TemplateResponse('friends.html', {"request": request,
                                                       "page_title": "Friends",
                                                       "friends": friends['data']['friends'],

                                                       })


@router.get("/search-friends/{query}", response_class=HTMLResponse)
async def search_friends_page(request: Request,
                              search_results: dict = Depends(search_users),
                              ):
    return templates.TemplateResponse('search_friends.html', {"request": request,
                                                              "page_title": "Search Friends",
                                                              "users": search_results['data'],

                                                              })
