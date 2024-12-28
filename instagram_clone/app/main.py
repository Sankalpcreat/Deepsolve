from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, post, comments

app = FastAPI(
    title="Instagram Clone API",
    description="A backend for an Instagram-like application built with FastAPI and MySQL.",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])

@app.get("/")
def root():
    return {"message": "Welcome to the Instagram Clone API!"}