from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.models.post import Post
from app.db.models.user import User
from app.db.session import async_session
from app.schemas.ai import AIReviewResponse, TopicSuggestion
from app.services.ai_service import ai_review, suggest_topics
from pydantic import BaseModel

router = APIRouter()

class ReviewPayload(BaseModel):
    title: str
    content: str


@router.post("/review", response_model=AIReviewResponse)
async def review(payload: ReviewPayload, user: str = Depends(get_current_user)):
    try:
        res = await ai_review(payload.title, payload.content)
        return res
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/topics", response_model=list[TopicSuggestion])
async def topics(user: str = Depends(get_current_user)):
    async with async_session() as session:
        query = select(Post, User).join(User, Post.author_id == User.id).where(User.id == user.get("id"))
        query = query.offset(0).limit(3)
        result = await session.execute(query)
        rows = result.all()
        titles = [post.title for post, user in rows if post.title]
        res = await suggest_topics(titles)
    return res
