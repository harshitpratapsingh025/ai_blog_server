from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.db.session import async_session
from app.schemas.user import UserCreate, UserLogin, Token
from app.db.models.user import User
from app.core.security import create_access_token, verify_password
from app.core.security import hash_password
from app.core.config import settings
from uuid import uuid4
from datetime import timedelta

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_in: UserCreate):
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.email == user_in.email))
            user = q.scalars().first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(
            id=uuid4(),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            username=user_in.username,
            email=user_in.email,
            password_hash=hash_password(user_in.password),
        )
        user = {
            "id": str(new_user.id),
            "name": f"{new_user.first_name} {new_user.last_name}",
            "username": new_user.username,
            "email": new_user.email,
        }
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        access_token = create_access_token(data={**user}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except Exception as e:
        print(f"Error during registration: {e}")  # For debugging purposes
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.email == user_in.email))
            user = q.scalars().first()
            auth_user = {
                    "id": str(user.id),
                    "name": f"{user.first_name} {user.last_name}",
                    "username": user.username,
                    "email": user.email,
                }
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        if not verify_password(user_in.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = create_access_token(data={**auth_user}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer", "user": auth_user}
    except Exception as e:
        print(f"Error during login: {e}")  # For debugging purposes
        raise HTTPException(status_code=500, detail="Something went wrong")
