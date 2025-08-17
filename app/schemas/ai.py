from pydantic import BaseModel
from typing import List

class ReviewSuggestion(BaseModel):
    severity: str  # e.g., "high", "medium", "low"
    type: str  # e.g., "grammar", "style", "content"
    message: str

class AIReviewResponse(BaseModel):
    suggestions: List[ReviewSuggestion]
    seoKeywords: List[str]
    readabilityScore: float


class TopicSuggestion(BaseModel):
    title: str
    description: str
    
class PostSummary(BaseModel):
    summary: str
    reading_time: int
