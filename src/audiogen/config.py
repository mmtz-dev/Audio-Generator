from __future__ import annotations

import torch
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings, loaded from environment variables."""

    model_config = {"env_prefix": "AUDIOGEN_", "env_file": ".env", "extra": "ignore"}

    # Device
    device: str = ""

    # Paths
    models_dir: str = "./models"
    trained_models_dir: str = "./checkpoints"
    outputs_dir: str = "./outputs"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Generation
    max_duration_seconds: int = 60
    audio_output_format: str = "wav"

    # MusicGen
    default_music_model: str = "facebook/musicgen-small"

    # HuggingFace
    hf_token: str = ""

    # Debug
    debug: bool = False

    def get_device(self) -> str:
        if self.device:
            return self.device
        return "cuda" if torch.cuda.is_available() else "cpu"


def get_settings() -> Settings:
    return Settings()
