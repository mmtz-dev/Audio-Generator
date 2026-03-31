from __future__ import annotations

import logging
import time

from audiogen.config import get_settings
from audiogen.core.audio_utils import tensor_to_wav
from audiogen.core.engine import AudioEngine, GenerationResult
from audiogen.core.file_manager import FileManager

logger = logging.getLogger(__name__)


class AudioGenEngine(AudioEngine):
    """Sound effects generation engine wrapping Meta's AudioCraft AudioGen."""

    name = "audiogen"
    engine_type = "sfx"
    required_vram_gb = 4.0  # audiogen-medium

    def __init__(self) -> None:
        super().__init__()
        self._model = None

    async def load(self, model_path: str | None = None) -> None:
        from audiocraft.models import AudioGen

        settings = get_settings()
        model_name = model_path or "facebook/audiogen-medium"
        device = settings.get_device()

        logger.info("Loading AudioGen model: %s on %s", model_name, device)
        self._model = AudioGen.get_pretrained(model_name, device=device)
        self._loaded = True

    async def unload(self) -> None:
        del self._model
        self._model = None
        self._loaded = False

    async def generate(
        self,
        prompt: str,
        duration_seconds: float = 10.0,
        temperature: float = 1.0,
        top_k: int = 250,
        top_p: float = 0.0,
        cfg_coef: float = 3.0,
        output_format: str = "wav",
        **kwargs,
    ) -> GenerationResult:
        if not self._model:
            raise RuntimeError("AudioGen model not loaded. Call load() first.")

        settings = get_settings()
        duration_seconds = min(duration_seconds, settings.max_duration_seconds)

        self._model.set_generation_params(
            use_sampling=True,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            duration=duration_seconds,
            cfg_coef=cfg_coef,
        )

        start = time.monotonic()
        audio = self._model.generate(descriptions=[prompt], progress=True)
        gen_time = time.monotonic() - start

        file_mgr = FileManager(settings)
        output_path = file_mgr.generate_output_path("sfx", output_format)
        sample_rate = self._model.sample_rate

        tensor_to_wav(audio[0], output_path, sample_rate)

        if output_format != "wav":
            from audiogen.core.audio_utils import convert_format
            output_path = convert_format(output_path, output_format, sample_rate)

        return GenerationResult(
            audio_path=output_path,
            duration_seconds=duration_seconds,
            sample_rate=sample_rate,
            engine_name=self.name,
            generation_time_seconds=round(gen_time, 2),
            metadata={"prompt": prompt},
        )
