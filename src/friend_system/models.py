from datetime import datetime

from sqlalchemy import Table, Column, Integer, TIMESTAMP, MetaData, ForeignKey
from src.auth.models import user

metadata = MetaData()

friendship = Table(
    "friendship",
    metadata,

    Column('user_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column('friend_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column("friendship_date", TIMESTAMP, default=datetime.utcnow, nullable=False)
)
