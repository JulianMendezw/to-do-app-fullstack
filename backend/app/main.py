from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routers.users import router as user_router
from app.routers.tasks import router as task_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(task_router)
