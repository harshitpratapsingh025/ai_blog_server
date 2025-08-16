import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = sa.Column(sa.String(50), nullable=True)
    last_name = sa.Column(sa.String(50), nullable=True)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    name = sa.Column(sa.Text, nullable=True)
    bio = sa.Column(sa.Text, nullable=True)
    avatar = sa.Column(sa.Text, nullable=True)
    password_hash = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
    )
