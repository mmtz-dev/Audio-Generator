from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException

from audiogen.api.dependencies import get_file_manager, get_model_manager
from audiogen.core.file_manager import FileManager
from audiogen.core.model_manager import ModelManager
from audiogen.schemas.requests import GenerationResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sfx", tags=["sfx"])


@router.post("/generate", response_model=GenerationResponse)
async def generate_sfx(
    prompt: Annotated[str, Form()],
    duration_seconds: Annotated[float, Form()] = 10.0,
    temperature: Annotated[float, Form()] = 1.0,
    top_k: Annotated[int, Form()] = 250,
    top_p: Annotated[float, Form()] = 0.0,
    cfg_coef: Annotated[float, Form()] = 3.0,
    output_format: Annotated[str, Form()] = "wav",
    mgr: ModelManager = Depends(get_model_manager),
    file_mgr: FileManager = Depends(get_file_manager),
):
    """Generate sound effects from a text prompt."""
    engine = await mgr.load_engine("audiogen")

    try:
        result = await engine.generate(
            prompt=prompt,
            duration_seconds=duration_seconds,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            cfg_coef=cfg_coef,
            output_format=output_format,
        )
    except Exception as e:
        logger.exception("SFX generation failed")
        raise HTTPException(status_code=500, detail=str(e))

    return GenerationResponse(
        audio_url=file_mgr.get_output_url(result.audio_path),
        duration_seconds=result.duration_seconds,
        sample_rate=result.sample_rate,
        engine_used=result.engine_name,
        generation_time_seconds=result.generation_time_seconds,
    )
