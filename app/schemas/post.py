from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from .user import UserRead


class PostCreate(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category: str
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = False
    reading_time: Optional[int] = 5


class PostRead(BaseModel):
    id: UUID
    author_id: UUID
    title: str
    content: str
    excerpt: str | None
    category: str
    tags: Optional[List[str]]
    is_published: bool
    likes_count: int = 0
    comments_count: int = 0
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    reading_time: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostWithAuthor(BaseModel):
    id: UUID
    authorId: UUID
    title: str
    content: str
    excerpt: str | None
    category: str
    tags: Optional[List[str]]
    isPublished: bool
    likesCount: int 
    commentsCount: int
    readingTime: int
    createdAt: datetime
    updatedAt: datetime
    imageUrl: Optional[str] = None
    audioUrl: Optional[str] = None
    author: UserRead

    class Config:
        orm_mode = True
