from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from audiogen.api.dependencies import get_file_manager, get_model_manager
from audiogen.core.file_manager import FileManager
from audiogen.core.model_manager import ModelManager
from audiogen.schemas.requests import GenerationResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/generate", response_model=GenerationResponse)
async def generate_voice(
    text: Annotated[str, Form()],
    engine: Annotated[str, Form()] = "chatterbox",
    # Chatterbox params
    exaggeration: Annotated[float, Form()] = 0.5,
    cfg_weight: Annotated[float, Form()] = 0.5,
    temperature: Annotated[float, Form()] = 0.8,
    # Bark params
    speaker_preset: Annotated[str | None, Form()] = None,
    text_temp: Annotated[float, Form()] = 0.7,
    waveform_temp: Annotated[float, Form()] = 0.7,
    # Shared
    output_format: Annotated[str, Form()] = "wav",
    reference_audio: UploadFile | None = File(None),
    mgr: ModelManager = Depends(get_model_manager),
    file_mgr: FileManager = Depends(get_file_manager),
):
    """Generate speech from text using Chatterbox or Bark."""
    audio_engine = await mgr.load_engine(engine)

    if engine == "chatterbox":
        gen_kwargs = {
            "text": text,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
            "output_format": output_format,
        }

        if reference_audio and reference_audio.filename:
            tmp = Path(tempfile.mktemp(suffix=".wav"))
            try:
                content = await reference_audio.read()
                tmp.write_bytes(content)
                gen_kwargs["reference_audio"] = tmp
                result = await audio_engine.generate(**gen_kwargs)
            finally:
                tmp.unlink(missing_ok=True)
        else:
            result = await audio_engine.generate(**gen_kwargs)

    elif engine == "bark":
        gen_kwargs = {
            "text": text,
            "speaker_preset": speaker_preset,
            "text_temp": text_temp,
            "waveform_temp": waveform_temp,
            "output_format": output_format,
        }
        try:
            result = await audio_engine.generate(**gen_kwargs)
        except Exception as e:
            logger.exception("Voice generation failed")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail=f"Unknown voice engine: {engine}")

    return GenerationResponse(
        audio_url=file_mgr.get_output_url(result.audio_path),
        duration_seconds=result.duration_seconds,
        sample_rate=result.sample_rate,
        engine_used=result.engine_name,
        generation_time_seconds=result.generation_time_seconds,
    )
