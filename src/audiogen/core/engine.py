from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GenerationResult:
    """Result from an audio generation engine."""

    audio_path: Path
    duration_seconds: float
    sample_rate: int
    engine_name: str
    generation_time_seconds: float
    metadata: dict = field(default_factory=dict)


class AudioEngine(ABC):
    """Abstract base class for all audio generation engines."""

    name: str = ""
    engine_type: str = ""  # "music", "voice", "sfx"
    required_vram_gb: float = 0.0

    def __init__(self) -> None:
        self._loaded = False

    @abstractmethod
    async def load(self, model_path: str | None = None) -> None:
        """Load model weights into memory."""

    @abstractmethod
    async def unload(self) -> None:
        """Unload model and free memory."""

    @abstractmethod
    async def generate(self, **kwargs) -> GenerationResult:
        """Generate audio. Keyword arguments vary by engine type."""

    def is_loaded(self) -> bool:
        return self._loaded
