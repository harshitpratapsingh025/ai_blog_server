import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.session import Base


class Like(Base):
    __tablename__ = "likes"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
