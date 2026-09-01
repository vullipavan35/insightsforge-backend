from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, datasets

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router)
api_router.include_router(datasets.router)
