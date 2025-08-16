import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import uuid4
from app.db.session import Base


class Post(Base):
    __tablename__ = "posts"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    author_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = sa.Column(sa.Text, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    excerpt = sa.Column(sa.Text, nullable=True)
    category = sa.Column(sa.Text, nullable=False)
    tags = sa.Column(ARRAY(sa.Text), nullable=False, server_default=sa.text("ARRAY[]::text[]"))
    is_published = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))
    likes_count = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    comments_count = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    reading_time = sa.Column(sa.Integer, nullable=False, server_default=sa.text("5"))
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
    )
