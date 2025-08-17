from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
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
async def topics(past_titles: str = ""):
    # past_titles is CSV; you can send array via query params from frontend
    titles = [t.strip() for t in past_titles.split(",") if t.strip()]
    res = await suggest_topics(titles)
    return res
