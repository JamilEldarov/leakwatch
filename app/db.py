from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Base


@lru_cache(maxsize=1)
def engine():
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def init_db() -> None:
    Base.metadata.create_all(engine())


def get_session() -> Session:
    return Session(engine())
