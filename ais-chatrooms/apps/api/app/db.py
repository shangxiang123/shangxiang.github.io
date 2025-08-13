from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import Settings

_engine = None
_SessionLocal = None


def init_engine(database_url: str):
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(database_url, pool_pre_ping=True, pool_size=5, max_overflow=10)
        _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def get_session() -> Session:
    if _SessionLocal is None:
        raise RuntimeError("DB not initialized. Call init_engine first.")
    return _SessionLocal()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()