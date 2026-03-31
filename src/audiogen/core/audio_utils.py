from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf
import torch


def tensor_to_wav(
    audio: torch.Tensor | np.ndarray,
    path: Path,
    sample_rate: int,
) -> Path:
    """Write an audio tensor to a WAV file.

    Accepts shapes: (samples,), (1, samples), or (channels, samples).
    """
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()

    # Squeeze batch dimension if present
    if audio.ndim == 3:
        audio = audio.squeeze(0)

    # soundfile expects (samples, channels) for multi-channel
    if audio.ndim == 2:
        audio = audio.T

    sf.write(str(path), audio, sample_rate)
    return path


def convert_format(
    input_path: Path,
    output_format: str,
    sample_rate: int | None = None,
) -> Path:
    """Convert an audio file to a different format (wav, mp3, flac, ogg)."""
    from pydub import AudioSegment

    audio = AudioSegment.from_file(str(input_path))

    if sample_rate:
        audio = audio.set_frame_rate(sample_rate)

    output_path = input_path.with_suffix(f".{output_format}")
    audio.export(str(output_path), format=output_format)

    # Remove original if different from output
    if input_path != output_path and input_path.exists():
        input_path.unlink()

    return output_path


def normalize_audio(audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
    """Peak-normalize audio to a target dB level."""
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    target_peak = 10 ** (target_db / 20)
    return audio * (target_peak / peak)


def get_audio_duration(path: Path) -> float:
    """Return the duration of an audio file in seconds."""
    info = sf.info(str(path))
    return info.duration
