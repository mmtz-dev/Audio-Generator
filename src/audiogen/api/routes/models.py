from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from audiogen.api.dependencies import get_model_manager
from audiogen.core.model_manager import ModelManager
from audiogen.schemas.requests import (
    CheckpointInfo,
    HealthResponse,
    ModelInfo,
    ModelListResponse,
)

router = APIRouter(tags=["models"])


@router.get("/models", response_model=ModelListResponse)
async def list_models(mgr: ModelManager = Depends(get_model_manager)):
    """List all available engines and their status."""
    engines = mgr.list_engines()
    return ModelListResponse(
        engines=[ModelInfo(**e) for e in engines],
        gpu=mgr.get_gpu_info(),
    )


@router.post("/models/{name}/load")
async def load_model(name: str, mgr: ModelManager = Depends(get_model_manager)):
    """Pre-load a specific engine into GPU memory."""
    try:
        await mgr.load_engine(name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "loaded", "engine": name}


@router.post("/models/{name}/unload")
async def unload_model(name: str, mgr: ModelManager = Depends(get_model_manager)):
    """Unload a specific engine from GPU memory."""
    try:
        await mgr.unload_engine(name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "unloaded", "engine": name}


@router.get("/checkpoints", response_model=list[CheckpointInfo])
async def list_checkpoints(mgr: ModelManager = Depends(get_model_manager)):
    """List trained model checkpoints from Audio-Trainer."""
    return [CheckpointInfo(**c) for c in mgr.scan_checkpoints()]


@router.get("/health", response_model=HealthResponse)
async def health(mgr: ModelManager = Depends(get_model_manager)):
    """Health check with GPU and model status."""
    engines = mgr.list_engines()
    loaded = [e["name"] for e in engines if e["loaded"]]
    return HealthResponse(
        status="healthy",
        gpu=mgr.get_gpu_info(),
        loaded_engines=loaded,
    )
