from fastapi import APIRouter
from typing import List
from datetime import datetime, timedelta
from uuid import uuid4

router = APIRouter()

# Mock data
mock_users = [
    {
        "id": str(uuid4()),
        "username": "john_doe",
        "email": "john@example.com",
        "name": "John Doe",
        "bio": "Full-stack developer and tech enthusiast",
        "avatar": None,
        "createdAt": datetime.now() - timedelta(days=30)
    },
    {
        "id": str(uuid4()),
        "username": "jane_smith",
        "email": "jane@example.com",
        "name": "Jane Smith",
        "bio": "UX designer and creative thinker",
        "avatar": None,
        "createdAt": datetime.now() - timedelta(days=25)
    }
]

mock_posts = [
    {
        "id": str(uuid4()),
        "authorId": mock_users[0]["id"],
        "title": "Getting Started with React and TypeScript",
        "content": "React with TypeScript is a powerful combination for building modern web applications...",
        "excerpt": "Learn how to set up a React project with TypeScript and start building type-safe components.",
        "category": "Technology",
        "tags": ["react", "typescript", "frontend"],
        "isPublished": True,
        "likesCount": 42,
        "commentsCount": 8,
        "readingTime": 5,
        "createdAt": datetime.now() - timedelta(days=5),
        "updatedAt": datetime.now() - timedelta(days=2),
        "author": mock_users[0]
    },
    {
        "id": str(uuid4()),
        "authorId": mock_users[1]["id"],
        "title": "Design Principles for Modern Web Apps",
        "content": "Good design is crucial for user experience. Here are some key principles...",
        "excerpt": "Explore essential design principles that will help you create better user experiences.",
        "category": "Design",
        "tags": ["design", "ux", "ui"],
        "isPublished": True,
        "likesCount": 28,
        "commentsCount": 12,
        "readingTime": 7,
        "createdAt": datetime.now() - timedelta(days=3),
        "updatedAt": datetime.now() - timedelta(days=1),
        "author": mock_users[1]
    },
    {
        "id": str(uuid4()),
        "authorId": mock_users[0]["id"],
        "title": "Building Scalable APIs with FastAPI",
        "content": "FastAPI is a modern Python framework for building APIs...",
        "excerpt": "Discover how to build high-performance APIs using FastAPI and Python.",
        "category": "Technology",
        "tags": ["python", "fastapi", "backend"],
        "isPublished": True,
        "likesCount": 35,
        "commentsCount": 6,
        "readingTime": 8,
        "createdAt": datetime.now() - timedelta(days=1),
        "updatedAt": datetime.now() - timedelta(hours=12),
        "author": mock_users[0]
    }
]

@router.get("/posts", response_model=List[dict])
async def get_mock_posts():
    """Mock endpoint that returns sample posts data"""
    return mock_posts

@router.get("/posts/{post_id}", response_model=dict)
async def get_mock_post(post_id: str):
    """Mock endpoint that returns a single post by ID"""
    for post in mock_posts:
        if post["id"] == post_id:
            return post
    return {"error": "Post not found"}

@router.post("/posts/{post_id}/like")
async def like_mock_post(post_id: str):
    """Mock endpoint for liking a post"""
    for post in mock_posts:
        if post["id"] == post_id:
            post["likesCount"] += 1
            return {"message": "Post liked successfully"}
    return {"error": "Post not found"}
