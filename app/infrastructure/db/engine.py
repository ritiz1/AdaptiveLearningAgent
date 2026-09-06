from __future__ import annotations

import os
from collections.abc import Iterator
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def _database_url() -> str:
    """Read DATABASE_URL, failing with a clear message when it is missing."""

    load_dotenv("app/.env")
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is missing from app/.env")
    return url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Return the shared engine, creating it on first use.

    Building the engine lazily keeps database configuration out of import
    time, so modules that merely import this package still work without a
    configured database.
    """

    return create_engine(
        _database_url(),
        pool_pre_ping=True,   # Containerised Postgres can drop idle connections.
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800,
    )


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Return the shared session factory.

    Callers that need a session should receive this factory rather than a
    live session, so they stay free to control session lifetime themselves.
    """

    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        expire_on_commit=False,
    )


def get_session() -> Iterator[Session]:
    """Provide a database session and close it afterward."""

    with get_session_factory()() as session:
        yield session
