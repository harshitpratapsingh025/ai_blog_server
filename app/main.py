from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.session import async_engine
from fastapi.staticfiles import StaticFiles
from app.api import users, posts, ai, auth, mock


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (if needed)


app = FastAPI(title="AI Blog — Backend", lifespan=lifespan)

origins = [
    "http://localhost:5173",  # React local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Only allow these domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="app/public"), name="public")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])


@app.get("/")
async def root():
    return {"message": "AI Blog backend running"}
