from __future__ import annotations

import os
from collections.abc import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


# Load DATABASE_URL from app/.env.
load_dotenv("app/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Fail early with a clear message if configuration is missing.
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from app/.env")


# The engine manages connections to PostgreSQL.
# It does not connect until a query is actually performed.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Creates short-lived database sessions for repositories/services.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Iterator[Session]:
    """Provide a database session and close it afterward."""

    with SessionLocal() as session:
        yield session
