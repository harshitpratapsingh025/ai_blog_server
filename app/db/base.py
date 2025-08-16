from app.db.session import Base

# import all models here so alembic can detect them
from app.db.models import user, post, comment, like  # noqa
from app.db.models import ai_review, ai_suggestion  # noqa
