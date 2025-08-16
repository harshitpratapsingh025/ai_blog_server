from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
import os

Base = declarative_base()

# Skip engine/session when running Alembic migrations
if not os.getenv("ALEMBIC_RUNNING"):
    async_engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
else:
    async_engine = None  # type: ignore
    async_session = None  # type: ignore
