from dotenv import load_dotenv
import os
load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


SECRET_AUTH = os.environ.get("SECRET_AUTH")


TMDB_API = os.environ.get("TMDB_API")
BASE_URL = os.environ.get("BASE_URL")


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")