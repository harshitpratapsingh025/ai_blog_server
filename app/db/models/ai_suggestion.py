import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4
from app.db.session import Base


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    suggestion_type = sa.Column(sa.String(50), nullable=False)
    data = sa.Column(JSONB, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
