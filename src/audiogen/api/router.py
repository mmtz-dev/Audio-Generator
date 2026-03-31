from fastapi import APIRouter

from audiogen.api.routes import models, music, sfx, voice

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(music.router)
api_router.include_router(voice.router)
api_router.include_router(sfx.router)
api_router.include_router(models.router)
