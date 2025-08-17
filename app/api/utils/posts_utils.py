from fastapi import HTTPException
from app.db.models.post import Post
from app.db.session import async_session
from sqlalchemy import select
from app.services.ai_service import ai_post_summarize

async def update_post_summary_and_reading_time(content: str, post_id: str):
    try:
        res = await ai_post_summarize(content)

        if not res or res is None:
            raise HTTPException(status_code=500, detail="AI service did not return valid summary or reading time")
        
        summary = res.get("summary", "")
        reading_time = res.get("reading_time", 0)
        
        async with async_session() as session:
            q = await session.execute(select(Post).where(Post.id == post_id))
            post = q.scalars().first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            post.excerpt = summary
            post.reading_time = reading_time
            await session.commit()

            return {"message": "Post summary and reading time updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
