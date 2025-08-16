from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Mark that Alembic is running so app code can adapt
os.environ["ALEMBIC_RUNNING"] = "1"

sys.path.append(os.path.abspath("."))

from app.db.base import Base  # noqa

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_sync_url() -> str:
    url = os.getenv("ALEMBIC_DATABASE_URL") or os.getenv("DATABASE_URL")
    return url.replace("+asyncpg", "") if url else None


def run_migrations_offline():
    url = get_sync_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(get_sync_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
