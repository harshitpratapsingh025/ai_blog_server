import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from uuid import uuid4
from app.db.session import Base


class AIReview(Base):
    __tablename__ = "ai_reviews"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_content = sa.Column(sa.Text, nullable=False)
    improved_content = sa.Column(sa.Text, nullable=False)
    readability_score = sa.Column(sa.Integer, nullable=False)
    seo_keywords = sa.Column(ARRAY(sa.Text), nullable=False, server_default=sa.text("ARRAY[]::text[]"))
    suggestions = sa.Column(JSONB, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
