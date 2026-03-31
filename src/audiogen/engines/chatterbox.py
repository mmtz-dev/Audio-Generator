from __future__ import annotations

import logging
import time
from pathlib import Path

import torchaudio

from audiogen.config import get_settings
from audiogen.core.engine import AudioEngine, GenerationResult
from audiogen.core.file_manager import FileManager

logger = logging.getLogger(__name__)


class ChatterboxEngine(AudioEngine):
    """Voice generation engine wrapping Resemble AI's Chatterbox TTS.

    Uses ChatterboxTTS (not Turbo) for full emotion control via the
    exaggeration parameter.
    """

    name = "chatterbox"
    engine_type = "voice"
    required_vram_gb = 2.0

    def __init__(self) -> None:
        super().__init__()
        self._model = None

    async def load(self, model_path: str | None = None) -> None:
        from chatterbox.tts import ChatterboxTTS

        settings = get_settings()
        device = settings.get_device()

        logger.info("Loading ChatterboxTTS on %s", device)
        self._model = ChatterboxTTS.from_pretrained(device)
        self._loaded = True

    async def unload(self) -> None:
        del self._model
        self._model = None
        self._loaded = False

    async def generate(
        self,
        text: str,
        reference_audio: str | Path | None = None,
        exaggeration: float = 0.5,
        cfg_weight: float = 0.5,
        temperature: float = 0.8,
        top_p: float = 1.0,
        repetition_penalty: float = 1.2,
        output_format: str = "wav",
        **kwargs,
    ) -> GenerationResult:
        if not self._model:
            raise RuntimeError("Chatterbox model not loaded. Call load() first.")

        settings = get_settings()

        gen_kwargs = {
            "text": text,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty,
        }

        if reference_audio:
            gen_kwargs["audio_prompt_path"] = str(reference_audio)

        start = time.monotonic()
        wav = self._model.generate(**gen_kwargs)
        gen_time = time.monotonic() - start

        sample_rate = self._model.sr
        duration_seconds = wav.shape[-1] / sample_rate

        file_mgr = FileManager(settings)
        output_path = file_mgr.generate_output_path("voice", "wav")
        torchaudio.save(str(output_path), wav, sample_rate)

        if output_format != "wav":
            from audiogen.core.audio_utils import convert_format
            output_path = convert_format(output_path, output_format, sample_rate)

        return GenerationResult(
            audio_path=output_path,
            duration_seconds=round(duration_seconds, 2),
            sample_rate=sample_rate,
            engine_name=self.name,
            generation_time_seconds=round(gen_time, 2),
            metadata={
                "text": text,
                "exaggeration": exaggeration,
                "has_reference": reference_audio is not None,
            },
        )
