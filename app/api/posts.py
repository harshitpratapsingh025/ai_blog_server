from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_user
from app.schemas.post import PostCreate, PostRead, PostWithAuthor
from app.db.models.post import Post
from app.db.models.user import User
from app.db.session import async_session
from sqlalchemy import select
from uuid import uuid4
from app.utils.post_utils import build_post_with_author

router = APIRouter()

@router.get("/my_posts", response_model=List[PostWithAuthor])
async def my_posts(user: str = Depends(get_current_user)):
    async with async_session() as session:
        print("Fetching posts for user:", user.get("id"))
        query = select(Post, User).join(User, Post.author_id == User.id).where(Post.author_id == user.get("id"))
        result = await session.execute(query)
        rows = result.all()
        return [build_post_with_author(post, author) for post, author in rows]


@router.get("/{post_id}", response_model=PostWithAuthor)
async def read_post(post_id: str):
    async with async_session() as session:
        q = await session.execute(
            select(Post, User)
            .join(User, Post.author_id == User.id)
            .where(Post.id == post_id)
        )
        result = q.first()
        if not result:
            raise HTTPException(status_code=404, detail="Post not found")
        
        post, author = result
        return build_post_with_author(post, author)




@router.post("/{post_id}/like")
async def like_post(post_id: str, user: str = Depends(get_current_user)):
    try:
        async with async_session() as session:
            q = await session.execute(select(Post).where(Post.id == post_id))
            post = q.scalars().first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            
            # For now, just increment the likes count
            # In a real app, you'd want to track individual likes in a separate table
            post.likes_count = (post.likes_count or 0) + 1
            await session.commit()
            
            return {"message": "Post liked successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@router.get("/", response_model=List[PostWithAuthor])
async def list_posts(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = Query(None)
):
    async with async_session() as session:
        query = select(Post, User).join(User, Post.author_id == User.id).where(Post.is_published == True)
        
        if category and category.lower() != "all":
            query = query.where(Post.category == category)
        
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        rows = result.all()

        return [build_post_with_author(post, author) for post, author in rows]

    
@router.post("/", response_model=PostRead)
async def create_post(payload: PostCreate, user: str = Depends(get_current_user)):
    async with async_session() as session:
        post = Post(
            id=uuid4(),
            author_id=user.get("id"),
            title=payload.title,
            content=payload.content,
            category=payload.category,
            tags=payload.tags or [],
            is_published=payload.is_published or False,
            reading_time=payload.reading_time or 5,
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post




