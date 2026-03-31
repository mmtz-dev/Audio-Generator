from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from audiogen.api.dependencies import get_file_manager, get_model_manager
from audiogen.core.file_manager import FileManager
from audiogen.core.model_manager import ModelManager
from audiogen.schemas.requests import GenerationResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/music", tags=["music"])


@router.post("/generate", response_model=GenerationResponse)
async def generate_music(
    prompt: Annotated[str, Form()],
    duration_seconds: Annotated[float, Form()] = 10.0,
    model_size: Annotated[str, Form()] = "small",
    temperature: Annotated[float, Form()] = 1.0,
    top_k: Annotated[int, Form()] = 250,
    top_p: Annotated[float, Form()] = 0.0,
    cfg_coef: Annotated[float, Form()] = 3.0,
    output_format: Annotated[str, Form()] = "wav",
    melody_audio: UploadFile | None = File(None),
    mgr: ModelManager = Depends(get_model_manager),
    file_mgr: FileManager = Depends(get_file_manager),
):
    """Generate music from a text prompt, optionally conditioned on a melody."""
    engine = await mgr.load_engine("musicgen")

    gen_kwargs = {
        "prompt": prompt,
        "duration_seconds": duration_seconds,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "cfg_coef": cfg_coef,
        "output_format": output_format,
    }

    if melody_audio and melody_audio.filename:
        import tempfile
        from pathlib import Path

        import torchaudio

        tmp = Path(tempfile.mktemp(suffix=".wav"))
        try:
            content = await melody_audio.read()
            tmp.write_bytes(content)
            waveform, sr = torchaudio.load(str(tmp))
            gen_kwargs["melody_audio"] = waveform
            gen_kwargs["melody_sample_rate"] = sr
        finally:
            tmp.unlink(missing_ok=True)

    try:
        result = await engine.generate(**gen_kwargs)
    except Exception as e:
        logger.exception("Music generation failed")
        raise HTTPException(status_code=500, detail=str(e))

    return GenerationResponse(
        audio_url=file_mgr.get_output_url(result.audio_path),
        duration_seconds=result.duration_seconds,
        sample_rate=result.sample_rate,
        engine_used=result.engine_name,
        generation_time_seconds=result.generation_time_seconds,
    )
