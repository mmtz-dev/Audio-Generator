from __future__ import annotations

import logging
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from audiogen.config import get_settings
from audiogen.core.engine import AudioEngine, GenerationResult
from audiogen.core.file_manager import FileManager

logger = logging.getLogger(__name__)


class BarkEngine(AudioEngine):
    """Voice generation engine wrapping Suno's Bark.

    Supports non-verbal sounds via inline tags: [laughs], [sighs],
    [clears throat], [music], ... (hesitation), and CAPS for emphasis.
    """

    name = "bark"
    engine_type = "voice"
    required_vram_gb = 6.0  # full model; small model ~2GB

    def __init__(self) -> None:
        super().__init__()
        self._sample_rate: int = 24000

    async def load(self, model_path: str | None = None) -> None:
        from bark import SAMPLE_RATE, preload_models

        logger.info("Loading Bark models...")
        preload_models()
        self._sample_rate = SAMPLE_RATE
        self._loaded = True

    async def unload(self) -> None:
        # Bark doesn't provide a clean unload; clear the module-level caches
        import bark.generation as bg

        for attr in ("_semantic_model", "_coarse_model", "_fine_model"):
            if hasattr(bg, attr):
                delattr(bg, attr)

        self._loaded = False

    async def generate(
        self,
        text: str,
        speaker_preset: str | None = None,
        text_temp: float = 0.7,
        waveform_temp: float = 0.7,
        output_format: str = "wav",
        **kwargs,
    ) -> GenerationResult:
        if not self._loaded:
            raise RuntimeError("Bark models not loaded. Call load() first.")

        from bark import generate_audio

        settings = get_settings()

        start = time.monotonic()
        audio_array = generate_audio(
            text,
            history_prompt=speaker_preset,
            text_temp=text_temp,
            waveform_temp=waveform_temp,
        )
        gen_time = time.monotonic() - start

        duration_seconds = len(audio_array) / self._sample_rate

        file_mgr = FileManager(settings)
        output_path = file_mgr.generate_output_path("voice", "wav")
        sf.write(str(output_path), audio_array, self._sample_rate)

        if output_format != "wav":
            from audiogen.core.audio_utils import convert_format
            output_path = convert_format(output_path, output_format, self._sample_rate)

        return GenerationResult(
            audio_path=output_path,
            duration_seconds=round(duration_seconds, 2),
            sample_rate=self._sample_rate,
            engine_name=self.name,
            generation_time_seconds=round(gen_time, 2),
            metadata={
                "text": text,
                "speaker_preset": speaker_preset,
            },
        )
