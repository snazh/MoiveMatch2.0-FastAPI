from datetime import datetime

from sqlalchemy import Table, Column, Integer, TIMESTAMP, MetaData, ForeignKey, Text, DECIMAL, String, JSON
from sqlalchemy.orm import relationship

from src.auth.models import user
from src.database import Base

metadata = MetaData()
movie = Table(
    'movie',
    metadata,
    Column("movie_id", Integer, primary_key=True),
    Column("details", JSON, nullable=False)
)
user_movie = Table(
    "user_movie",
    metadata,
    Column("user_id", Integer, ForeignKey(user.c.id), primary_key=True),
    Column("movie_id", Integer, ForeignKey(movie.c.movie_id), primary_key=True),
    Column("added_at", TIMESTAMP, default=datetime.utcnow)
)

comment = Table(
    "comment",
    metadata,
    Column("user_id", Integer, ForeignKey(user.c.id), primary_key=True),
    Column("movie_id", Integer, ForeignKey(movie.c.movie_id), primary_key=True),
    Column("content", Text, nullable=False),
    Column("rating", DECIMAL(3, 1), nullable=True),
    Column("posted_at", TIMESTAMP, default=datetime.utcnow)
)
