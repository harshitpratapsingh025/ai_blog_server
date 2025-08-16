import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.session import Base


class Comment(Base):
    __tablename__ = "comments"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    author_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = sa.Column(sa.Text, nullable=False)
    parent_id = sa.Column(UUID(as_uuid=True), nullable=True)
    likes_count = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
