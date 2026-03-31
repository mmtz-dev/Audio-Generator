from __future__ import annotations

from pydantic import BaseModel, Field


# ── Request models ──────────────────────────────────────────────


class MusicRequest(BaseModel):
    prompt: str = Field(..., description="Text description of the music to generate")
    duration_seconds: float = Field(10.0, ge=1.0, le=300.0)
    model_size: str = Field("small", pattern="^(small|medium|large|melody)$")
    temperature: float = Field(1.0, ge=0.0, le=2.0)
    top_k: int = Field(250, ge=0, le=1000)
    top_p: float = Field(0.0, ge=0.0, le=1.0)
    cfg_coef: float = Field(3.0, ge=0.0, le=10.0)
    output_format: str = Field("wav", pattern="^(wav|mp3|flac|ogg)$")


class VoiceRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize as speech")
    engine: str = Field("chatterbox", pattern="^(chatterbox|bark)$")
    # Chatterbox-specific
    exaggeration: float = Field(0.5, ge=0.0, le=2.0)
    cfg_weight: float = Field(0.5, ge=0.0, le=2.0)
    temperature: float = Field(0.8, ge=0.0, le=2.0)
    # Bark-specific
    speaker_preset: str | None = Field(None, description="Bark voice preset, e.g. v2/en_speaker_1")
    text_temp: float = Field(0.7, ge=0.0, le=2.0)
    waveform_temp: float = Field(0.7, ge=0.0, le=2.0)
    # Shared
    output_format: str = Field("wav", pattern="^(wav|mp3|flac|ogg)$")


class SFXRequest(BaseModel):
    prompt: str = Field(..., description="Text description of the sound effect to generate")
    duration_seconds: float = Field(10.0, ge=1.0, le=60.0)
    temperature: float = Field(1.0, ge=0.0, le=2.0)
    top_k: int = Field(250, ge=0, le=1000)
    top_p: float = Field(0.0, ge=0.0, le=1.0)
    cfg_coef: float = Field(3.0, ge=0.0, le=10.0)
    output_format: str = Field("wav", pattern="^(wav|mp3|flac|ogg)$")


# ── Response models ─────────────────────────────────────────────


class GenerationResponse(BaseModel):
    audio_url: str
    duration_seconds: float
    sample_rate: int
    engine_used: str
    generation_time_seconds: float


class ModelInfo(BaseModel):
    name: str
    type: str
    loaded: bool
    required_vram_gb: float


class ModelListResponse(BaseModel):
    engines: list[ModelInfo]
    gpu: dict


class CheckpointInfo(BaseModel):
    name: str
    path: str
    format: str
    size_mb: float


class HealthResponse(BaseModel):
    status: str
    gpu: dict
    loaded_engines: list[str]
