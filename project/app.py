from fastapi import FastAPI
from project.routers.users import router as users_router
from project.routers.posts import router as posts_router

app = FastAPI()

app.include_router(posts_router(), prefix="/posts", tags=['posts'])
app.include_router(posts_router(), prefix="/users", tags=['users'])