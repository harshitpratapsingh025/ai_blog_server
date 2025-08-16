from app.db.models.post import Post
from app.db.models.user import User


def build_post_with_author(post: Post, author: User) -> dict:
    """Convert SQLAlchemy Post + User to camelCase response dict"""
    return {
        "id": post.id,
        "authorId": post.author_id,
        "title": post.title,
        "content": post.content,
        "excerpt": post.excerpt,
        "category": post.category,
        "tags": post.tags,
        "isPublished": post.is_published,
        "likesCount": post.likes_count,
        "commentsCount": post.comments_count,
        "readingTime": post.reading_time,
        "createdAt": post.created_at,
        "updatedAt": post.updated_at,
        "author": {
            "id": author.id,
            "username": author.username,
            "email": author.email,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "bio": author.bio,
            "avatar": author.avatar,
            "createdAt": author.created_at
        }
    }
