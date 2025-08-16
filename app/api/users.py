from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password, get_current_user
from app.db.session import async_session
from app.db.models.user import User
from sqlalchemy import select
from uuid import uuid4

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(payload: UserCreate, user: str = Depends(get_current_user)):
    async with async_session() as session:
        # basic uniqueness checks
        q = await session.execute(
            select(User).where(
                (User.email == payload.email) | (User.username == payload.username)
            )
        )
        exists = q.scalars().first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User exists"
            )
        user = User(
            id=uuid4(),
            username=payload.username,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@router.get("/email/{email}", response_model=UserRead)
async def get_by_email(email: str, user: str = Depends(get_current_user)):
    async with async_session() as session:
        q = await session.execute(select(User).where(User.email == email))
        user = q.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@router.get("/", response_model=list[UserRead])
async def get_all_users(user: str = Depends(get_current_user)):
    async with async_session() as session:  
        q = await session.execute(select(User))
        users = q.scalars().all()
        return users

